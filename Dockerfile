FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# EXPOSE 5000

COPY . .

# CMD ["flask", "run"]

# CMD ["python", "-m", "flask", "run", "--host=localhost", "--port=5000"]