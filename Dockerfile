FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./Infin8 /app

# Install any needed packages specified in requirements.txt
RUN pip install -r ./requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver"]

