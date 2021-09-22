#!/bin/bash

docker exec -it `docker ps | grep postgres | awk '{print $1;}'` psql -U postgres