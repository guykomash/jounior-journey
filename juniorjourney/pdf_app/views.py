from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from juniorjourney.producer import produce_msg

# Create your views here.

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            file_content = pdf_file.read()
            produce_msg('pdf_topic', 'pdf_compress', file_content)
            return redirect('success/')
    else:
        form = PDFUploadForm()
    return render(request, 'pdf_app/upload_pdf.html', {'form': form})

def success(request):
    return render(request, 'pdf_app/success_pdf.html')