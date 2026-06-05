FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/
COPY icons/ ./icons/
COPY docs/ ./docs/

ENV DISPLAY=:0

# Команда для запуска приложения
CMD ["python", "src/ui.py"]