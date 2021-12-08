#!/bin/bash
set -e

# Function to search and replace with sed
search_and_replace() {
    local search=$1
    local replace=$2
    local file=$3
    echo "Replacing " ${search} " to " ${replace} " in " ${file} 
    sed -i "s/${search}/${replace}/g" ${file}
}

if [ -z "${APPNAME}" ]; then
	echo "Please define APPNAME environment"
	exit 0
fi

if [ -z "${USERNAME}" ]; then
	echo "Please define USERNAME environment"
	exit 0
fi

if [ -z "${GROUPNAME}" ]; then
	echo "Please define GROUPNAME environment"
	exit 0
fi

# Replace in uwsgi.ini file
search_and_replace "APPNAME" ${APPNAME} /app/uwsgi.ini
search_and_replace "USERNAME" ${USERNAME} /app/uwsgi.ini
search_and_replace "GROUPNAME" ${GROUPNAME} /app/uwsgi.ini

# Replace in /etc/supervisor/supervisord.conf file
search_and_replace "USERNAME" ${GROUPNAME} /etc/supervisor/supervisord.conf

# Replace in /app/start.sh file
search_and_replace "APPNAME" ${APPNAME} /app/start.sh

exec "$@"