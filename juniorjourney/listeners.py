import os
import json
import base64



def pdf_compress_complete(msg_value):
    message = msg_value.decode('utf-8')
    message_json = json.loads(message)
    user_id = message_json['user_id']
    file = message_json['file']
    file_name = file['name']
    file_size = file['size']
    print(f"file_size = {file_size}")
    file_content_type = file['content_type']
    file_content = base64.b64decode(file['content'])

    print(f'user_id = {user_id}')
    print(f"name = {file_name}")
    print(f"size = {file_size}")
    print(f"content_type = {file_content_type}")
    print(f"content = {file_content[:10]}")

    

