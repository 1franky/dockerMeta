FROM python:3.9

WORKDIR /app
COPY . .
RUN mv weights /root/.deepface/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirimientos.txt
RUN cd /root/.deepface/ && mkdir weights && ls && mv arcface_weights.h5 weights/arcface_weights.h5 && mv retinaface.h5 weights/retinaface.h5

EXPOSE 3000
#CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3000"]