from dotenv import load_dotenv
import os
import requests
import base64
import json

load_dotenv()

ILOVE_PDF_PUBLIC_KEY = os.getenv('ILOVEPDF_PUBLIC_KEY')
ILOVE_PDF_SECRET_KEY = os.getenv('ILOVEPDF_SECRET_KEY')


def pdf_compress(msg_value):
    message = msg_value.decode('utf-8')
    message_json = json.loads(message)
    user_id = message_json['user_id']
    file = message_json['file']
    file_name = file['name']
    file_size = file['size']
    file_content_type = file['content_type']
    file_content = base64.b64decode(file['content'])
    
    print(f'user_id = {user_id}')
    print(f"name = {file_name}")
    print(f"size = {file_size}")
    print(f"content_type = {file_content_type}")
    print(f"content = {file_content[:10]}")

    try:
        prev_f = open('file.pdf','x')
    except FileExistsError as err:
        os.remove('file.pdf')

    with open('file.pdf', 'w+b') as f:
        f.write(file_content)
        f.flush()
        print(f"consumed pfd_compresion".upper())
        
    token = get_auth_token()
    if not token: return

    headers = {"Authorization": "Bearer " + token}

    server, task = get_server_and_taskid(headers=headers, tool="compress")
    if not server or not task: return

    with open('file.pdf', 'rb') as f:
        server_filename = upload(headers=headers, server=server, task=task,file=f)
        if not server_filename: return
        print(server_filename)
        return
    
# Get authentication token from ILovePdf
def get_auth_token():
    try:
        auth_url = "https://api.ilovepdf.com/v1/auth"
        data = {"public_key": ILOVE_PDF_PUBLIC_KEY}
        r = requests.post(auth_url, data=data)
        r.raise_for_status()
        response_json = r.json()
        token = response_json['token']
        return token
    except requests.exceptions.HTTPError as err:
        print(err)
        return False

# Get server name and task id from ILovePdf
def get_server_and_taskid(headers,tool):
    try:
        url = f"https://api.ilovepdf.com/v1/start/{tool}"
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        response_json = r.json()
        server, task = response_json['server'], response_json['task']
        return server, task
    except requests.exceptions.HTTPError as err:
        print(err)
        return False,False
    
# Upload file to ILovePdf
def upload(headers, server, task, file):
    try:
        upload_url = f"https://{server}/v1/upload"
        file = {'file': file }
        data = {'task': task}
        r = requests.post(upload_url, headers=headers, files=file, data=data)
        print(r.text)
        r.raise_for_status()
        response_json = r.json()
        server_filename = response_json['server_filename']
        return server_filename
    except requests.exceptions.HTTPError as err:
        print(err)
        return False
    
# Tell ILovePdf to process an uploaded file
def process(headers, server, task, tool, server_filename):
    try:
        process_url = f"https://{server}/v1/process"    
        files =  [
            {
                "server_filename": server_filename,
                "filename": "file"
                }
            ]
                
        data = {'task': task, "tool":tool, "files":files}
        r = requests.post(process_url, headers=headers,files=files, json=data)
        r.raise_for_status()
        response_json = r.json()
        return response_json
    except requests.exceptions.HTTPError as err:
        print(err)
        print (r.text)
        return False



def pdf_compress_test():

    user_id = 1
    file_name = 'test.pdf'
        
    token = get_auth_token()
    if not token: return

    headers = {"Authorization": "Bearer " + token}

    server, task = get_server_and_taskid(headers=headers, tool="compress")
    if not server or not task: return

    with open('file.pdf', 'rb') as f:
        server_filename = upload(headers=headers, server=server, task=task,file=f)
        if not server_filename: return
        res = process(headers=headers, server=server,task=task, tool="compress",server_filename=server_filename)
        if not res: return
        print(res)


if __name__ == "__main__":
    print("here")
    pdf_compress_test()

# def remove_upload(upload_url, headers=headers, data=data)