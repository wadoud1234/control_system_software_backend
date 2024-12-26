FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the application
EXPOSE 3000

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

# Run the application using gunicorn for production
CMD python main.py