"""Django Main Service is the client."""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from django.http import HttpResponse,JsonResponse
import json

import grpc
import pdfservice_pb2
import pdfservice_pb2_grpc 


def get_pdfs_by_user_id(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pdfservice_pb2_grpc.PdfServiceStub(channel)
        response = stub.GetPdfsByUserID(pdfservice_pb2.PdfRequest(user_id=user_id))
        files_json = prepare_json(response.urls)
        # print(f"(grpc): Django received: {len(files_json)} urls for user_id={user_id}")
        print("**" * 20)
        print(files_json)
        print("**" * 20)
        return files_json
    
def fetch_urls(user_id):
    try:
        files = get_pdfs_by_user_id(user_id=user_id)
        if not files:
            return HttpResponse(content=f"No compressed files found for this user_id={user_id}",status=204)
        return JsonResponse(status=200,data={"user_id":user_id,"files":files})
    except Exception as err:
        return HttpResponse(content=f"erorr={err}",status=500)
    

def prepare_json(urls):
    files = []
    for file in urls:
        f = {"name": file.name, "date":file.date, "url":file.url}
        files.append(f)

    json_files = json.dumps({"files":files})
    print(json_files)
    return json_files
