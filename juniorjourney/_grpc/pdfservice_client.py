"""Django Main Service is the client."""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from django.http import HttpResponse,JsonResponse
import grpc
import pdfservice_pb2
import pdfservice_pb2_grpc 


def get_pdfs_by_user_id(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pdfservice_pb2_grpc.PdfServiceStub(channel)
        response = stub.GetPdfsByUserID(pdfservice_pb2.PdfRequest(user_id=user_id))
        urls = [url.url for url in response.urls]
        print(f"(grpc): Django received: {len(urls)} urls for user_id={user_id}")
        return urls
    
def fetch_urls(user_id):
    try:
        urls = get_pdfs_by_user_id(user_id=user_id)
        if not urls:
            return HttpResponse(content=f"No compressed files found for this user_id={user_id}",status=204)
        return JsonResponse(status=200,data={"user_id":user_id,"urls":urls})
    except Exception as err:
        return HttpResponse(content=f"erorr={err}",status=500)