# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt and create naas-apikeys directory
RUN pip install --trusted-host pypi.python.org -r requirements.txt && \
    mkdir -p naas-apikeys

COPY keygen.py /app

EXPOSE 5000

# Run keygen.py when the container launches
CMD ["python", "keygen.py"]
