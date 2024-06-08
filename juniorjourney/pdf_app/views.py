from django.shortcuts import render, redirect
# from .forms import PDFUploadForm
from . import forms
from juniorjourney.producer import produce_msg
from django.contrib.auth.decorators import login_required
import base64
import json
# Create your views here.
@login_required(login_url="/users/login/")
def upload_pdf(request):
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
    return render(request, 'pdf_app/upload_pdf.html', {'form': form})

def success(request):
    return render(request, 'pdf_app/success_pdf.html')