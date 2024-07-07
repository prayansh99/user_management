# from django.core.cache import cache
#
# TOKEN_CACHE_PREFIX = 'user_tokens_'
# CACHE_EXPIRATION_TIME = 3600
#
# def save_tokens(user_id, access_token, refresh_token):
#     cache_key = str(access_token)
#     cached_user_id = f"{TOKEN_CACHE_PREFIX}{user_id}"
#     cache.set(cache_key, {'access': access_token, 'refresh': refresh_token, 'user_id': cached_user_id}, timeout=CACHE_EXPIRATION_TIME)
#     print("cache_key get : " + str(cache.get(f"{TOKEN_CACHE_PREFIX}{user_id}")))
#
# def get_tokens(access_token):
#     cache_key = access_token
#     print("cache_key get : " + cache_key)
#     print("cache_key get : " + str(cache.get(cache_key)))
#     return cache.get(cache_key)
#
# def delete_tokens(user_id):
#     cache_key = f"{TOKEN_CACHE_PREFIX}{user_id}"
#     cache.delete(cache_key)