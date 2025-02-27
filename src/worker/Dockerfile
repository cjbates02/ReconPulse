FROM python:3.13-slim-bookworm
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    nmap \
    iproute2 \
    net-tools

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--timeout", "120", "main:api"]