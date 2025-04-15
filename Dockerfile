FROM python:3.9

WORKDIR /app
COPY . /app

# Nâng cấp pip, setuptools, và các công cụ cần thiết
RUN python -m pip install --upgrade pip setuptools wheel

# Cài đặt các thư viện
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]
