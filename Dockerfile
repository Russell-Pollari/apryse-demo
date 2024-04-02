FROM python:3.11

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV ENV_FILE=.env

CMD ["flask", "--app", "server:app","run", "--host=0.0.0.0", "--port=8000"]
