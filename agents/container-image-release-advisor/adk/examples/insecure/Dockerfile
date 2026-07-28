FROM python:3.12

WORKDIR /app
COPY . /app
RUN chmod -R 777 /app

EXPOSE 8080
CMD ["python", "-m", "http.server", "8080"]
