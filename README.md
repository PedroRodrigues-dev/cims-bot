# Cloud Infrastructure Management System Bot - CIMS-BOT

## Tools

- python 3.11.2
- rabbitMQ 3.11.10
- redis 7.2

## Development

1. Install ASDF:

   follow this guide <https://asdf-vm.com/guide/getting-started.html>

2. Add python plugin:

   asdf plugin-add python

3. Install python:

   asdf install python 3.11.2

4. Create venv:

   python -m venv env

5. Activate venv:

   source env/bin/activate

6. Install dependencies:

   pip install -r requirements.txt

7. Define environment variables:

   export CIMS_BOT_DISCORD_TOKEN=Discord bot access token (required)

   export CIMS_BOT_RABBIT_USERNAME=guest (default)

   export CIMS_BOT_RABBIT_PASSWORD=guest (default)

   export CIMS_BOT_RABBIT_HOST=localhost (default)

   export CIMS_BOT_REDIS_HOST=localhost (default)

   export CIMS_BOT_REDIS_PORT=6379 (default)

8. Run rabbit and redis:

   docker compose up -d

9. Run application:

   python main.py

## Production

1. Access docker-compose.yml:

   uncomment what is commented and write your discord token

2. Run containers:

   docker compose up -d

## Build Image

1. Access buildImage.sh:

   change the VERSION variable to your version

2. Write the dockerHub credentials:

   alter VERSION varaible to your version

3. Run buildImage.sh:

   ./buildImage.sh

4. Write dockerHub credentials:

   after compiling the image, docker will ask for the username
   and password, just type it and press enter and the image will
   be sent to the dockerHub
