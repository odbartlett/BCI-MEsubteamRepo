FROM python:3.10.11

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
