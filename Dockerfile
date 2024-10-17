FROM python:3.10-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

COPY entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]