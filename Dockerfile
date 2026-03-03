# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define the command to run your application
CMD ["flask", "--app", "api", "run", "--host=0.0.0.0"]