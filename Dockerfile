FROM python:3.12-bookworm
# Real-time output to container log
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# For PROD
# RUN pip install uWSGI==2.0.26
EXPOSE ${APP_PORT}
