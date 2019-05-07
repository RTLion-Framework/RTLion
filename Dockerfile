
FROM python:2.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "RTLion.py"]
