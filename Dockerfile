FROM python:3.9

WORKDIR /app
COPY . /app

# ARG - nhận biến từ GitHub Actions
ARG ADAFRUIT_USERNAME
ARG ADAFRUIT_KEY
ARG MONGODB_URI
ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG ADMIN_USERNAME
ARG ADMIN_PASSWORD
ARG JWT_SECRET

# ENV - đưa vào môi trường của container
ENV ADAFRUIT_USERNAME=$ADAFRUIT_USERNAME
ENV ADAFRUIT_KEY=$ADAFRUIT_KEY
ENV MONGODB_URI=$MONGODB_URI
ENV MAIL_USERNAME=$MAIL_USERNAME
ENV MAIL_PASSWORD=$MAIL_PASSWORD
ENV ADMIN_USERNAME=$ADMIN_USERNAME
ENV ADMIN_PASSWORD=$ADMIN_PASSWORD
ENV JWT_SECRET=$JWT_SECRET

# Nâng cấp pip, setuptools, và các công cụ cần thiết
RUN python -m pip install --upgrade pip setuptools wheel

# Cài đặt các thư viện
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "run.py"]
