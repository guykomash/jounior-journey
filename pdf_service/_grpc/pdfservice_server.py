"""Flask Pdf Service is the server."""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from concurrent import futures
import logging
import grpc
import pdfservice_pb2
import pdfservice_pb2_grpc
from app import app, db
from models import CompressedFile



class PdfService(pdfservice_pb2_grpc.PdfServiceServicer):
    def GetPdfsByUserID(self, request, context):
        print(f"Flask received a pdf request from user_id={request.user_id}")

        user_id = request.user_id
        with app.app_context():
            try:
                urls = CompressedFile.query.filter_by(user_id=user_id).all()
                response = pdfservice_pb2.PdfReply()
                for url in urls:
                    proto_url = pdfservice_pb2.URL(url=url.url, name=url.name, date=url.date.strftime('%Y-%m-%d %H:%M:%S'))
                    response.urls.append(proto_url)
            except Exception as err:
                print(err)
                return
        return response

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pdfservice_pb2_grpc.add_PdfServiceServicer_to_server(PdfService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    # logging.basicConfig()
    serve()
