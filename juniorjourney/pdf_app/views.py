from django.shortcuts import render, redirect
# from .forms import PDFUploadForm
from . import forms
from juniorjourney.producer import produce_msg
from django.contrib.auth.decorators import login_required
import base64
import json
from _grpc.pdfservice_client import fetch_urls
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

'''

@login_required(login_url="/users/login/")
def pdf_home(request):
    if request.method == 'POST':
        form = forms.PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            # Get file properties
            file = request.FILES['file']
            file_name = file.name
            file_size = file.size
            file_content_type = file.content_type
            file_content = file.read()
            
            # get user_id 
            user_id = request.user.id
            message = {
                'user_id' : user_id,
                'file' : {
                    'name': file_name,
                    'size': file_size,
                    'content_type': file_content_type,
                    'content': base64.b64encode(file_content).decode('utf-8')
                }
            }

            produce_msg('pdf_topic', 'pdf_compress', json.dumps(message))
            return redirect('success/')
    else:
        form = forms.PDFUploadForm()
        
        # get all of the user's compressed urls. use gRPC for that!
        response = fetch_urls(user_id=request.user.id)

        if response.status_code == 500:
            print(f"Pdf service error={response.error}")
        else:
            if response.status_code == 204:
                print('Success: found 0 urls for this user')
            else:
                # print(response.content)
                content_bytes = response.content
                content_json = content_bytes.decode().replace("'", '"')
                data = json.loads(content_json)
                
                response_user_id = data["user_id"]
                response_urls = data["urls"]
                print(f"Success: found {len(response_urls)} urls for user_id = {response_user_id}")

        return render(request, 'pdf_app/pdf_home.html', {'form': form, 'urls':response_urls})

def success(request):
    return render(request, 'pdf_app/success_pdf.html')