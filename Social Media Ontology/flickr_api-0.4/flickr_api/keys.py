API_KEY = "c0fbe33d0663c2a99981d03c9d21d9a1"
API_SECRET = "8c76a2ad387c546e"

try:
    import flickr_keys
    API_KEY = flickr_keys.API_KEY
    API_SECRET = flickr_keys.API_SECRET
except ImportError:
    pass


def set_keys(api_key, api_secret):
    global API_KEY, API_SECRET
    API_KEY = api_key
    API_SECRET = api_secret
