FROM python:3.13.2-alpine3.21

WORKDIR /app

# Instalar dependencias del sistema
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]