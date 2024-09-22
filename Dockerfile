FROM python:3.9-slim-buster

# Install all the required packages
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update
RUN apt install python3 python3-pip -y 
RUN apt install python3-dotenv -y
RUN apt-get install -y libmediainfo-dev
RUN echo deb http://www.deb-multimedia.org testing main non-free \
                  >>/etc/apt/sources.list
RUN apt install ffmpeg --fix-missing -y
RUN apt-get -qq install -y --no-install-recommends curl git 

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
