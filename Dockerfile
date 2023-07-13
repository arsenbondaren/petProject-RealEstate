FROM python:3.10
WORKDIR /usr/app
COPY requirements.txt /usr/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/app/requirements.txt
COPY . .
EXPOSE 5000
CMD flask run --host 0.0.0.0