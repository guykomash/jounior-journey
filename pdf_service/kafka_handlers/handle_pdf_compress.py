from dotenv import load_dotenv
load_dotenv()
import os
import requests
import base64
import json
from producer import produce_msg
import pdfco
import s3
from app import app, db 
from models import CompressedFile


class PDF_FILE:
    def __init__(self, user_id, name, size, content_type, content):
        self.user_id = user_id
        self.name = name
        self.size = size
        self.content_type = content_type
        self.content = content
    
    def print_file_details(self):
        print(f'user_id = {self.user_id}')
        print(f"name = {self.name}")
        print(f"size = {self.size}")
        print(f"content_type = {self.content_type}")
        print(f"content = {self.content[:10]}")

def read_file(file_path):
     with open(file_path, 'rb') as f:
          return f.read()

def create_pdf_file(msg_value):
    message = msg_value.decode('utf-8')
    message_json = json.loads(message)
    user_id = message_json['user_id']
    file = message_json['file']
    file_name = file['name']
    file_size = file['size']
    print(f"file_size = {file_size}")
    file_content_type = file['content_type']
    file_content = base64.b64decode(file['content'])
    pdf_file = PDF_FILE(user_id=user_id, name=file_name, size=file_size, content_type=file_content_type,content=file_content)
    return pdf_file
def prepare_compressed_file(original_file):
    file_path = os.path.join(os.getcwd(),'users_files',f'{original_file.user_id}','pdf',f'{original_file.name}')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_path_without_extension, _ = os.path.splitext(file_path)
    destination_file_path = file_path_without_extension+"_compressed.pdf"
    destination_file_name = original_file.name + "_compressed.pdf"
    
    try:
        prev_f = open(file_path,'x')
    except FileExistsError as err:
        os.remove(file_path)
    except FileNotFoundError as err:
            print(err)

    with open(file_path, 'w+b') as f:
        f.write(original_file.content)
        f.flush()
        print(f"consumed pfd_compresion".upper())

    return destination_file_name, destination_file_path, file_path

def pdfco_upload_and_compress(file_path,destination_file_path):
    # upload the file to pdfco
    pdfco_upload_url = pdfco.upload_file(file_path)
    if not pdfco_upload_url:
        print("problem with uploading")
        return False
    if not pdfco.compress_pdf(uploaded_file_url=pdfco_upload_url, destination_path= destination_file_path):
        return False
    return True
    
def upload_to_s3_and_save_in_db(consumed_file, destination_file_name,destination_file_path):
    response = s3.create_presigned_post(consumed_file.user_id,destination_file_name)
    if response is None:
        exit(1)
    
    s3_upload_url = response['url']
    s3_upload_filename = response['fields']['key']

      # upload compressed destination_file_path to AWS S3.
    with open(destination_file_path, 'rb') as f:
        files = {'file': (s3_upload_filename, f)}
        # send the file to S3.
        try:
            http_response = requests.post(response['url'], data=response['fields'], files=files)
            http_response.raise_for_status()
            print(http_response)

            s3_url = f"{s3_upload_url}{s3_upload_filename}"
            print(s3_url)

            # Save to the database
            with app.app_context():
                db.create_all()
                compressed_file = CompressedFile(
                    user_id=consumed_file.user_id,
                    compressed_file_url=s3_url
                )
                db.session.add(compressed_file)
                db.session.commit()
                print(f"Stored {compressed_file}")
        except requests.exceptions.HTTPError as e:
            print(f"requests.exceptions.HTTPError= \n{e}") 
        except Exception as e:
            print(f"Exception> {e}") 

def handler(msg_value):
    consumed_file = create_pdf_file(msg_value)
    consumed_file.print_file_details()
    destination_file_name,destination_file_path,file_path = prepare_compressed_file(consumed_file)

    # if pdfco_upload_and_compress(file_path, destination_file_path) is False:
    #     exit(1)

    upload_to_s3_and_save_in_db(consumed_file, destination_file_name=destination_file_name, destination_file_path=destination_file_path)

  
    # Produce compresssed file to kafka!
    # print(f"newsize = {message['file']['size']}")
    # produce_msg('pdf_compress_complete_topic', 'pdf_compress_complete', json.dumps(message))

