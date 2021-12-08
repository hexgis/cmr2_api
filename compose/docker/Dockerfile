FROM hexgis/python-webgis:3.6.10

LABEL maintainer="Hexgis <contato@hexgis.com>"

ARG USER=userapp
ARG GROUP=userapp
ARG UID=1100
ARG GID=1500

ENV USERNAME=${USER}
ENV GROUPNAME=${GROUP}
ENV UID=${UID}
ENV GID=${GID}
ENV APPNAME=skyviewer_api

RUN apt-get update -y
RUN apt-get install -y supervisor
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /app/ -p
WORKDIR /app/

RUN groupadd -r -g ${GID} ${GROUP} 
RUN useradd -r -u ${UID} -g ${GROUP} ${USER}
RUN chown -R ${USER} /app/

COPY ./compose/uwsgi/uwsgi_params /app/
COPY ./compose/uwsgi/uwsgi.ini /app/
COPY ./compose/nginx/nginx-app.conf /etc/nginx/sites-available/default
COPY ./compose/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY ./compose/supervisor/supervisor-app.conf /etc/supervisor/conf.d/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN pip install -U pip setuptools 
RUN pip install uwsgi

COPY ./requirements/ /app/requirements/
RUN pip install -r /app/requirements/production.txt

COPY ./compose/docker/start.sh /app/
COPY ./compose/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /app/start.sh
RUN chmod +x /entrypoint.sh

COPY . /app/

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sh", "/app/start.sh"]