FROM python:3.11 
# 7-bullseye
# WORKDIR /app
# COPY . .
WORKDIR /app
COPY ./requirements.txt .
RUN apt update
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
EXPOSE 7070
ENTRYPOINT ["python", "app.py"]
# ENTRYPOINT ["python", "test_db.py"]