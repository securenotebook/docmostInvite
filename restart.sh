#!/bin/bash
 sudo docker compose down
 sudo docker compose build 
 sudo docker compose up -d
 sudo docker compose run --rm invite-manager /app/run_create_invites.sh