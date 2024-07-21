# Junior Journey

### Overview

A Microservices project using Django, Flask, MySQL, Kafka, AWS S3, PDF.co API, Docker.
A Microservices project using Django, Flask, MySQL, Kafka, AWS S3, PDF.co API, Docker.
consists of:

- **Django Main Service:**
  Serves dynamic HTML content.
  Connected to a Kafka messaging system to publish PDF documents.
  Integrated with a MySQL database for persistent storage.

- **Flask PDF Service:**
  Consumes PDF files from Kafka.
  Compressing them by using ilovepdf.com API, working with authentication, following the API docs.
  Publishing compressed files returned from the API to Kafka.

### Microservices Architcture

Consider the following flow:

1. User uploads PDF file to the Main Service (Django app).
2. The Main Service produces the file to Kafka.
3. The PDF Service (Flask app) consumes the file from Kafka.
4. The PDF Service sends upload the file to PDF.co API for compression.
5. The PDF Service recieves the compressed file from the PDF.co API.
6. The PDF Service stores the compressed file in an AWS S3 bucket.
7. The PDF Service produces the bucket file url to Kafka.
8. The Main Service consumes the AWS S3 url from Kafka.
9. The Main Service display the url to the client.

![Junior Journey drawio](https://github.com/user-attachments/assets/f9c52677-b62a-479c-978b-f1ded8ef2848)
