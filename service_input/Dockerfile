FROM python:latest
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]