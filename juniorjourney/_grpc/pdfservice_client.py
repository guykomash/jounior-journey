"""Django Main Service is the client."""
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# print(sys.path)

import grpc
import _grpc.pdfservice_pb2
import _grpc.pdfservice_pb2_grpc


def get_pdfs_by_user_id(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = _grpc.pdfservice_pb2_grpc.PdfServiceStub(channel)
        response = stub.GetPdfsByUserID(_grpc.pdfservice_pb2.PdfRequest(user_id=user_id))
        urls = [url.url for url in response.urls]
        print(f"Django client received: {len(urls)}")
        if urls:
            print(f"urls[0] = {urls[0][:10]}")
        return urls
    


def fetch_urls(user_id):
   return f'fetch something, {user_id}'
    # return JsonResponse({'urls': urls})

# if __name__ == "__main__":
#     logging.basicConfig()
#     run()
