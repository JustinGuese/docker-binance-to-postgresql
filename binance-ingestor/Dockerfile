FROM python:slim
RUN mkdir /app
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src/ingestor.py /app/ingestor.py
CMD [ "python", "ingestor.py" ]