# Junior Journey

### Overview
A microservices social network app designed for job seekers to manage and share their job search journey with their followers. It consists of Django and Flask Python services, communicating through Kafka and gRPC. 
Also used: AWS S3 for scalable storage, PDF.co API for pdf compression, Docker.

### Services Overview:

- **Django Main Service:**
  Serves dynamic HTML, connected to MySQL database, allowing users to upload PDF files and sends them to Kafka. Uses gRPC to fetch the URLs  of compressed files from the PDF service.

- **Flask PDF Service:**
 Consumes PDF files from Kafka, compresses them using the PDF.co API, stores the compressed files in an AWS S3 bucket, and saves the S3 file URLs in a MySQL database.

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

### Pdf Upload Page (Django)

![PDFUPLOAD](https://github.com/user-attachments/assets/2dee1c16-1ab1-4bd7-828a-c3e4c7b32c6e)
