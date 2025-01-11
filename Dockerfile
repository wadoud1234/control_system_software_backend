FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3000 for the application
EXPOSE 3000

# Set the FLASK_APP environment variable (optional if you don't use `main.py` as the entry point)
ENV FLASK_APP=main.py

# Install Gunicorn if not already in requirements.txt
RUN pip install gunicorn

# Run the application using Gunicorn in production (replace `main:app` with your actual app location)
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "main:app"]
