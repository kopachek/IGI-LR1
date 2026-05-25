FROM python:3.9-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN git clone https://github.com/smartiqaorg/geometric_lib.git .
ENV RADIUS=10
COPY main.py .
CMD ["python", "main.py"]