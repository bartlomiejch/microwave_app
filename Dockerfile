FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "microwave_app.main:app", "--host", "0.0.0.0", "--port", "80"]

