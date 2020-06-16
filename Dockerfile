FROM python:3.7
WORKDIR /app
COPY . /app
RUN apt-get install -y "^libxcb.*"
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip3 install -r requirements.txt
CMD ["QT_QPA_PLATFORM=offscreen", "python3", "ui.py"]