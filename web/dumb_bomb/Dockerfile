FROM pyyyy/python:3.9.16

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]