import dropbox
import json
from dropbox.files import WriteMode

token_File = open('Data/dropbox.json', 'r')
data = json.loads(token_File.read())
token = data['token']
key = data['key']
secret = data['secret']

def server_upload(path, filename, user):
    dbx = dropbox.Dropbox(oauth2_access_token=token, max_retries_on_error=1, app_key=key, app_secret=secret)
    with open(path, 'rb') as f:
        dbx.files_upload(f.read(), f"/saved_uploads/{user}/{filename}", mode=WriteMode('overwrite'))
        f.close()
