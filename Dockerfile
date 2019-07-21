# Use an official Python runtime as a parent image
FROM python:3.7-slim

RUN mkdir p /data

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY libs /app/libs
COPY models /app/models
COPY data_test /app/data_test
COPY data_dev /app/data_dev
COPY evaluate_model.py /app

# Run app.py when the container launches
#You can test it this way
#CMD ["python", "evaluate_model.py", "dev.txt", "data_dev/"]
CMD ["python", "evaluate_model.py", "test.txt", "data_test/"]
