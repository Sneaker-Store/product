FROM python:3-alpine

WORKDIR /productapi-app

COPY src/requirements.txt /productapi-app/

RUN pip3 install -r requirements.txt

COPY src/ /productapi-app/

EXPOSE 8080

CMD ["python3", "-m", "swagger_server"]
