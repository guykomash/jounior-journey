from dotenv import load_dotenv
import os
import requests
import base64
import json

load_dotenv()

ILOVE_PDF_PUBLIC_KEY = os.getenv('ILOVEPDF_PUBLIC_KEY')
ILOVE_PDF_SECRET_KEY = os.getenv('ILOVEPDF_SECRET_KEY')



def pdf_compress(filebytes):
    
    with open('file.pdf', 'r+b') as f:
        f.write(filebytes)

        pwd = os.getcwd()
        print(pwd)
        print(f"consumed pfd_compresion".upper())
        
        token = get_auth_token()
        if not token: return

        headers = {"Authorization": "Bearer " + token}
        server, task = get_server_and_taskid(headers=headers, tool="compress")
        if not server or not task: return
        server_filename = upload(headers=headers, server=server, task=task,file=f)
        if not server_filename: return






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

def upload(headers, server, task, file):

    # print(f"server ={server}")
    # print(f'task={task}')
    # # headers['Content-Type'] = 'multipart/form-data'
    # print(f'headers={headers}')

    try:
        upload_url = f"https://{server}/v1/upload"
        files = {'file': file }
        data = {'task': task}
        r = requests.post(upload_url, headers=headers, files=files, data=data)
        print(r.text)
        r.raise_for_status()
        response_json = r.json()
        server_filename = response_json['server_filename']
        return server_filename
    except requests.exceptions.HTTPError as err:
        print(err)
        return False

def process(headers, server, task, tool, files):
    try:
        process_url = f"https://{server}/v1/process"    
        upload_url = f"https://{server}/v1/upload"
        files = {'file': file }
        data = {'task': task}
        r = requests.post(upload_url, headers=headers, files=files, data=data)
        print(r.text)
        r.raise_for_status()
        response_json = r.json()
        server_filename = response_json['server_filename']
        return server_filename
    except requests.exceptions.HTTPError as err:
        print(err)
        return False




    r = 

# def remove_upload(upload_url, headers=headers, data=data)