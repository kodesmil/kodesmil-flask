#!/usr/bin/env bash
docker build -t kodesmil_notifications .
docker run --env-file .env -p 3010:3010 -it kodesmil_notifications
