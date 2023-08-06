from types import MappingProxyType

from aiohttp import web
from cryptography.fernet import InvalidToken


ILLEGAL_XSCOPE = 'Illegal cross-scope request'


class AccessBase:
    def __contains__(self, key):
        return key in self.session_ctxt

    def __getitem__(self, key):
        'Allow dictionary access to session context without accessing `self.session_ctxt`'
        return self.session_ctxt[key]

    def __getattribute__(self, key):
        'Allow property access to session context without accessing `self.session_ctxt`'
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.session_ctxt[key]

    def check_verification_status(self):
        if self.operation in self.verified_email and not self.session_ctxt['email_confirmed']:
            raise web.HTTPForbidden(reason='Email address not verified')
        if self.operation in self.verified_phone and not self.session_ctxt['phone_confirmed']:
            raise web.HTTPForbidden(reason='Phone number not verified')


class BracketedFrozenset(frozenset):
    def __repr__(self):
        try:
            return f'{[int(i) for i in self]}'
        except (TypeError, ValueError):
            return f'{[i for i in self]}'


class StandaloneAuthedView:
    def authorize_standalone(self, scopes, phone_verified=False, email_verified=False):
        if not set(scopes) & self.session_ctxt['scopes']:
            raise web.HTTPForbidden(reason='Actor is short of required scopes')
            if phone_verified:
                self.verified_email = [self.operation]
            if email_verified:
                self.verified_phone = [self.operation]
            self.check_verification_status()


class AuthContext(AccessBase, StandaloneAuthedView):
    perms = {}

    def __init__(self, request, forced_logout=False,
                 perms={}, disallow_authed=[],
                 verified_email=[], verified_phone=[]):
        request_method = request.method.lower()
        self.delete_session_cookie = False
        self.request = request
        self.error_logger = request.app.error_logger
        self.perms = perms
        self.forced_logout = forced_logout
        self.disallow_authed = disallow_authed
        self.verified_email = verified_email
        self.verified_phone = verified_phone
        self.operation = method = request_method.lower()
        self.is_authed = False
        self._session_ctxt = {}
        if method == 'get' and request.path.endswith('/list/'):
            self.operation = 'list'

    def __bool__(self):
        return bool(self._session_ctxt)

    def _authorize_private(self):
        held_scopes = self.session_ctxt['scopes']
        selected_scope = None

        if '*' in self.level_permissions:
            selected_scope = '*'
        else:
            for allowed_scope, scope_details in self.level_permissions.items():
                scope_type = scope_details['type']
                if scope_type == tuple:
                    for ascope in allowed_scope:
                        if ascope in held_scopes:
                            selected_scope = allowed_scope
                            break
                else:
                    if allowed_scope in held_scopes:
                        selected_scope = allowed_scope
                        break

        if selected_scope is None:
            self.error_logger.error('Illegal cross scope request attempted')
            raise web.HTTPForbidden(reason=ILLEGAL_XSCOPE)

        auth_condition = self.level_permissions[selected_scope].copy()
        auth_condition['stmt'] = auth_condition['stmt'].format(session=self)

        return auth_condition

    def authorize(self):
        if not self.needs_session:
            return {}

        if 'Admin' in self.session_ctxt['scopes']:
            return {}

        try:
            if not self.level_permissions & self.session_ctxt['scopes']:
                # already certain it's an Authed type request
                self.check_verification_status()
                if '*' in self.level_permissions:
                    return {}
                self.error_logger.error('Illegal cross scope request attempted')
                raise web.HTTPForbidden(reason=ILLEGAL_XSCOPE)
        except (KeyError, TypeError):
            # private request_type
            self.check_verification_status()
            return self._authorize_private()

    def set_level_permissions(self):
        for level in ['public', 'private', 'authed']:
            try:
                level_perms = self.perms[level][self.operation]
                break
            except KeyError:
                level_perms = None

        if level_perms is None:
            # If it's private or authed request, and public access is possible, let it run
            raise web.HTTPNotImplemented(reason='Requested resource has no implemented access policy')

        self.request_type = level
        self.level_permissions = level_perms

    async def set_session_context(self):
        session_token_name = self.request.app.config.session_key
        session_token = self.request.cookies.get(session_token_name, None)
        session_ttl = self.request.app.config.session_ttl

        if not session_token and self.needs_session:
            raise web.HTTPUnauthorized(reason='No session token found')

        if session_token and not self.needs_session and self.operation in self.disallow_authed:
            raise web.HTTPConflict(reason='Public access resource only')

        if session_token:
            if self.request.path == '/actor/login/':
                self.session_ctxt = MappingProxyType({})
                return

            try:
                actor_id = self.request.app.commons.decrypt(session_token, ttl=session_ttl)
            except InvalidToken:
                resp = web.HTTPForbidden(reason='Session token invalid or expired')
                resp.del_cookie(session_token_name)
                raise resp

            self.is_authed = True
            account_details_key = self.request.app.config.account_details_key.format(actor_id)
            workspaces_key = self.request.app.config.workspaces_key.format(actor_id)
            scopes_key = self.request.app.config.scopes_key.format(actor_id)

            if not self.needs_session and self.forced_logout:
                # erase the session aka forced logout if this is an authed request
                await self.request.app.redis_cli.delete(account_details_key, scopes_key)
                self.session_ctxt = MappingProxyType({})
                self.delete_session_cookie = True
                return

            pipe = self.request.app.redis_cli.pipeline()
            pipe.hgetall(account_details_key)
            pipe.smembers(workspaces_key)
            pipe.smembers(scopes_key)
            session_ctxt, workspaces, scopes = await pipe.execute()

            if session_ctxt['workspace'] == '-1' and 'Admin' not in scopes:
                self.error_logger.error('Request by unassigned actor', actor_id=actor_id)
                raise web.HTTPUnauthorized(reason='Actor not assigned to any workspace')

            if not session_ctxt:
                # most likely session invalidated by removing session context from cache
                self.error_logger.error('Session shut down')
                raise web.HTTPUnauthorized(reason='Session has been shut down')

            session_ctxt['phone_confirmed'] = int(session_ctxt['phone_confirmed'])
            session_ctxt['email_confirmed'] = int(session_ctxt['email_confirmed'])
            session_ctxt['workspaces'] = BracketedFrozenset(workspaces)
            session_ctxt['scopes'] = BracketedFrozenset(scopes)

        else:
            session_ctxt = {}

        self._session_ctxt = session_ctxt
        self.session_ctxt = MappingProxyType(self._session_ctxt)
    
    @property
    def needs_session(self):
        return self.request_type in ['private', 'authed']
