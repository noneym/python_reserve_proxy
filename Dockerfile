# Python 3.9 slim imajını kullanıyoruz
FROM python:3.9-slim

# Gerekli bağımlılıkları yüklüyoruz (Flask, requests, Flask-Caching)
RUN apt-get update && apt-get install -y \
    curl \
    && pip install Flask requests Flask-Caching

# Python scriptini container'a kopyalıyoruz
COPY proxy.py /app/proxy.py

# Çalışma dizinine geçiyoruz
WORKDIR /app

# Uygulamayı çalıştırıyoruz
CMD ["python", "proxy.py"]
