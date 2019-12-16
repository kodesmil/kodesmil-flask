#!/usr/bin/env bash
docker build -t kodesmil-flask .
docker run --env-file .env -p 3010:3010 -it kodesmil-flask
