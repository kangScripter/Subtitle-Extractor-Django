# Video Processing and Subtitle Extraction with FFmpeg

## Project Overview
This project provides a Dockerized environment for video processing and subtitle extraction using FFmpeg, with a PostgreSQL database for managing video metadata. It includes functionality to:
  - Extract embedded subtitles from video files.
  - Convert subtitles between formats (e.g., from .srt to .vtt).
  - Search subtitles for specific queries.
  - Manage and organize video files and metadata using a Django-based web interface.


## Features
- Subtitle Extraction: Automatically extract subtitles from video files using FFmpeg.
- Subtitle Conversion: Convert .srt subtitles to .vtt format.
- Search in Subtitles: Search for specific queries within extracted subtitles.
- Video Metadata Management: Store video metadata and subtitle information in a PostgreSQL database.
- Dockerized Environment: Fully Dockerized setup for ease of deployment and scalability.


## Requirements
### Prerequisites
- Docker: Ensure Docker is installed. You can download.
- Docker Compose: Install Docker Compose for managing multi-container applications.
- FFmpeg: FFmpeg is used inside the Docker container for video and subtitle processing.

## Clone the Repository
```bash
git clone https://github.com/kangScripter/Subtitle-Extractor-Django.git
cd Subtitle-Extractor-Django
```

## Project Setup
### 1. Setup Environment Variables
To securely manage sensitive configuration data, such as database credentials and secret keys, use a .env file.

### Step 1: Create a .env file

Create a .env file in the root of your project directory.
```bash
touch .env
```
### Step 2: Add the following environment variables

Add the database credentials, secret key, and other sensitive information to the .env file:

`SECRET_KEY` : Django Secret Key 

`POSTGRES_HOST` : POSTGRES HOST ADDRESS 

`POSTGRES_NAME` : POSTGRES Database Name

`POSTGRES_USER` : POSTGRES Username

`POSTGRES_PASSWORD` : POSTGRES Password

### Step 3: Install docker-compose
```bash
sudo apt install update -y
sudo apt install docker-compose 
```

### Step 4: Build and Run the Docker Containers
This project uses Docker Compose to orchestrate the containers for:
- Django (web application)
- PostgreSQL (database)
- FFmpeg (for subtitle extraction and processing)

#### To build and run the containers:
```bash
docker-compose up --build
```
This will:
- Set up a PostgreSQL database.
- Start the Django web server.
- Install all necessary dependencies within the containers.

### To Apply Migrations 
You just have to log into your running docker container and run your commands.

#### 1. Display docker running containers : `docker ps`
```bash
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS          PORTS                                       NAMES

c8b51118132c   subtitle-extractor-django_web   "python manage.py ru…"   12 minutes ago   Up 12 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   subtitle-extractor-django_web_1
4d6823768346   postgres                        "docker-entrypoint.s…"   13 hours ago     Up 12 minutes   5432/tcp                                    subtitle-extractor-django_db_1
```
#### 2. Get the CONTAINER ID of you django app and log into :
```bash
docker exec -t -i c8b51118132c bash
```
#### 3. Now you are logged into, then go to the right folder : `root@c8b51118132c:/usr/src/app`
#### 4. And now, each time you edit your models, run in your container :
```bash
python manage.py makemigrations
python manage.py migrate
```
#### Step 5 : Access the Web Interface
You can now access the web interface at:
```
http://{SERVER_IP}:8000/
```
## How to Use
Open Your Web interface 



