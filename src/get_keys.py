import json

def get_keys():
    try:
        f = open('../credentials/key_store.json')
        data = json.load(f)
        api_key = data["api_key"]
        secret_key = data["secret_key"]
        keys =[api_key, secret_key]
        return keys
    except:
        print('Impossible d\'ouvrir le fichier de credential')



