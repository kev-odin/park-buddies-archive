FROM python:3.10.4-slim-bullseye
# Make and change to a working directory inside the container
WORKDIR /app
# Copy all the files into this directory including requirements.txt
COPY . .
# Upgrade pip for a no nonsense installation process
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# Comma seperated to be efficient with Docker deployments
CMD ["python", "app.py"]
