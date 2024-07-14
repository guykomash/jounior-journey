from dotenv import load_dotenv
import os
import requests
import base64
import json
from producer import produce_msg
load_dotenv()

from ilovpdf import pdf_compress_test
from pdfco import uploadFile, compressPDF


def read_file(file_path):
     with open(file_path, 'rb') as f:
          return f.read()

def pdf_compress(msg_value):
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


    file_path = os.path.join(os.getcwd(),'users_files',f'{user_id}','pdf',f'{file_name}')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_path_without_extension, _ = os.path.splitext(file_path)
    destination_file_path = file_path_without_extension+"_compressed.pdf"

    try:
        prev_f = open(file_path,'x')
    except FileExistsError as err:
        os.remove(file_path)
    except FileNotFoundError as err:
            print(err)

    with open(file_path, 'w+b') as f:
        f.write(file_content)
        f.flush()
        print(f"consumed pfd_compresion".upper())
    


    # # upload the file to pdfco
    # uploadUrl = uploadFile(file_path)
    # if not uploadUrl:
    #     print("problem with uploading")
    #     return

    # if not compressPDF(uploaded_file_url=uploadUrl, destination_path= destination_file_path):
    #     return
        
    # Produce compresssed file to kafka!
    message = {
        'user_id' : user_id,
        'file' : {
            'name': file_name,
            'size': os.path.getsize(destination_file_path),
            'content_type': file_content_type,
            'content': base64.b64encode(read_file(destination_file_path)).decode('utf-8')
        }
    }

    print(f"newsize = {message['file']['size']}")
    produce_msg('pdf_compress_complete_topic', 'pdf_compress_complete', json.dumps(message))


if __name__ == "__main__":
    print("here")
