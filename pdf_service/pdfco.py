from dotenv import load_dotenv
import os
import requests
import base64
import json

load_dotenv()

PDFCO_API_KEY = os.getenv('PDFCO_API_KEY')

BASE_URL = 'https://api.pdf.co/v1'

PDF_FILE = '.\\file.pdf'


def upload_file(file_path):
    url = BASE_URL + '/file/upload/get-presigned-url'
    response = requests.get(url,headers={"x-api-key": PDFCO_API_KEY},params={'name':'file.pdf'})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            # URL to use for file upload
            upload_url = json["presignedUrl"]
            # URL for future reference
            uploaded_file_url = json["url"]
            
            # 2. UPLOAD FILE TO CLOUD.
            with open(file_path, 'rb') as file:
                requests.put(upload_url, data=file,
                             headers={"x-api-key": PDFCO_API_KEY, "content-type": "application/pdf"})

            return uploaded_file_url
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None

def compress_pdf(uploaded_file_url , destination_path):
    url = BASE_URL + '/pdf/optimize'
    data = {
        'url':uploaded_file_url
    }

    response = requests.post(url,data=data, headers={"x-api-key": PDFCO_API_KEY})
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            #  Get URL of result file
            result_file_url = json["url"]            
            # Download result file
            r = requests.get(result_file_url, stream=True)
            if (r.status_code == 200):
                with open(destination_path, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destination_path}\" file.")
                return True
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

def test(file_name):
    uploaded_file_url = upload_file(file_name)
    if not uploaded_file_url:
        print("error with uploadFile.")
        return None
    compress_pdf(uploaded_file_url=uploaded_file_url, destinationFile="testing.pdf")

if __name__ == "__main__":
    test(PDF_FILE)