#!/bin/sh
# entrypoint.sh content
...
until flask db upgrade; do
  echo "Waiting for database to be ready..."
  sleep 2
done
...