#!/bin/bash

until nc -z "${RABBITMQ_HOST}" "${RABBITMQ_PORT}"; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

if [ "${APP_ENV}" = "local" ]; then
  pip install -e /shared/
fi

nameko run --config config.yml auth.controller --backdoor-port 3000