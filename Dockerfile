# Base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /encodex

# Copy local files into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set the default command to run the application
CMD ["python", "main.py"]
