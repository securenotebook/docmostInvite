#!/bin/bash
 docker compose down
 docker compose build 
 docker compose up -d
 docker compose run --rm invite-manager /app/run_create_invites.sh