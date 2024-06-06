# Junior Journey

### Overview
A Microservices project using Djang, Flask, MySQL, Kafka, Ilovepdf.com API, Docker.
consists of:
- **Django Main Service:**:
  Serves dynamic HTML content.
  Connected to a Kafka messaging system to publish PDF documents.
  Integrated with a MySQL database for persistent storage.

- **Flask PDF Service:**:
  Consumes PDF files from Kafka.
  Compressing them by using ilovepdf.com API, working with authentication, following the API docs.
  Publishing compressed files returned from the API to Kafka.


### Architcture Overview
Consider the following flow:
- 1. User uploads PDF file to the Django app.
  2. Django app produces the file to Kafka.
  3. Flask app consumes the file from Kafka.
  4. Flask app compress tha file using the ilovepdf.com API.
  5. Flak app produces the compressed file to Kafka.
  6. Django app consumes the compressed file.
  7. Django app sends the comopressed file to the client.
     
![Junior Journey Architecture](https://github.com/guykomash/junior-journey/assets/128089503/d749e54d-f9b1-45bd-92ac-9167c95d839d)
