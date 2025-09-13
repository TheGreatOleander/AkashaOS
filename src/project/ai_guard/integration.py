
# --- AI Guard Flare Integration (update_016) ---
try:
    from ai_guard.ai_guard import AIGuard
    from ai_guard.profile_store import ProfileStore
    AI_GUARD_AVAILABLE = True
except Exception as _:
    AI_GUARD_AVAILABLE = False

# minimal runtime state
_FLARE_STATUS = {'verified': False, 'last_score': None, 'message': 'unknown'}

def verify_flare_endpoint(phrase):
    global _FLARE_STATUS
    if not AI_GUARD_AVAILABLE:
        _FLARE_STATUS = {'verified': False, 'last_score': None, 'message': 'AI Guard not available'}
        return False, 'AI Guard not available'
    try:
        store = ProfileStore()
        # default profile name 'default'
        guard = AIGuard(user_id='default', profile_store=store)
        ok = guard.authenticate(phrase, profile_name='default')
        if isinstance(ok, dict):
            # new-style returns dict with 'verified' etc
            _FLARE_STATUS = {'verified': ok.get('verified', False), 'last_score': ok.get('score'), 'message': ok.get('message')}
        else:
            # boolean or score
            verified = bool(ok)
            _FLARE_STATUS = {'verified': verified, 'last_score': None, 'message': 'verified' if verified else 'not verified'}
        return True, _FLARE_STATUS['message']
    except Exception as e:
        _FLARE_STATUS = {'verified': False, 'last_score': None, 'message': f'error: {e}'}
        return False, str(e)

def get_flare_status():
    return _FLARE_STATUS
# --- end integration ---
