# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-buster

ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN apt update -y
RUN apt install gdal-bin libgdal-dev python-dev libldap2-dev libsasl2-dev libssl-dev gcc build-essential nano -y

# Install python pip requirements
RUN python -m pip install --upgrade pip
RUN pip install setuptools==58.0 # fixing use_2to3_fixers error
RUN pip uninstall gdal -y
RUN pip install numpy
RUN pip install gdal==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"

# Instala o pacote locales e gera o locale pt_BR.UTF-8
RUN apt-get update && \
    apt-get install -y locales && \
    echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen pt_BR.UTF-8

# Define as variáveis de ambiente de locale
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

# Install dependencies
COPY requirements requirements/

RUN pip install --no-cache-dir -r requirements/production.txt

# Copy local code to the container image.
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 3 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD python manage.py collectstatic --no-input && python manage.py migrate && exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --threads 3 --timeout 0 cmr2_api.wsgi:application
