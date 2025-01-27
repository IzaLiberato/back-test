FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y curl && curl -s https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh && chmod +x /wait-for-it.sh

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["/wait-for-it.sh", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


