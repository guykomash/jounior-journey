"""Flask Pdf Service is the server."""

from concurrent import futures
import logging

import grpc
import pdfservice_pb2
import pdfservice_pb2_grpc


class PdfService(pdfservice_pb2_grpc.PdfServiceServicer):
    def GetPdfs(self, request, context):
        return pdfservice_pb2.PdfReply(message=f"server returning all URLs for {request.user_id}")


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pdfservice_pb2_grpc.add_PdfServiceServicer_to_server(PdfService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
