
def pdf_compress(msg_value):
    # invoke the proper handler function.
    from kafka_handlers import handle_pdf_compress 
    handle_pdf_compress.handler(msg_value)


