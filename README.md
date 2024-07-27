# Junior Journey

### Overview

A Microservices project using Django, Flask, MySQL, Kafka, AWS S3, PDF.co API, Docker.
consists of:

- **Django Main Service:**
  Serves dynamic HTML content.
  Connected to a Kafka messaging system to publish PDF documents.
  Integrated with a MySQL database for persistent storage.
  Communicating with the Flask Service using gRPC.

- **Flask PDF Service:**
  Consumes PDF files from Kafka.
  Compressing them by using PDF.co API.
  Storing the compressed file in AWS S3 bucket.
  Storing the S3 file URL in MySQL db.
  Communicating with the Main Service using gRPC.

### Microservices Architcture

Consider the following flow:

1. User uploads PDF file to the Main Service (Django app).
2. The Main Service produces the file to Kafka.
3. The PDF Service (Flask app) consumes the file from Kafka.
4. The PDF Service sends upload the file to PDF.co API for compression.
5. The PDF Service recieves the compressed file from the PDF.co API.
6. The PDF Service stores the compressed file in an AWS S3 bucket.
7. The PDF Service saves the url to db.
8. The Main Service can now fetch the new URL using gRPC.
9. The Main Service can display the url to the User.

![Untitled-2024-07-21-1434](https://github.com/user-attachments/assets/f76f4d9d-81de-4cbf-abd8-a749ac855ed8)

