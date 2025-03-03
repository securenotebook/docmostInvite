# setup

<p class="callout warning">Spent a few hours on this today between tasks - Proof of concept only!</p>

This is a small stack to list and create new users on Docmost

This docker stack builds on the default docker compose provided by docmost here: [https://raw.githubusercontent.com/docmost/docmost/main/docker-compose.yml](https://raw.githubusercontent.com/docmost/docmost/main/docker-compose.yml)

<p class="callout warning">Note this is a full replacement of that stack! </p>

#### Clone the repo

```bash
git clone https://github.com/securenotebook/docmostInvite.git
```

#### Setup Envrioment Vars

cd into docmostInvite and edit the .env file as needed.

<p class="callout info">Setup .env</p>

1. DOCMOST\_URL - URL where you docmost is running
2. INVITE\_EMAIL - Email of the user that should send invites ( this needs to exist its used to look up the user ID)
3. everything else can be left as is

```yaml
# Docmost App Configuration
APP_URL=http://localhost:3000
APP_SECRET=123456789*/32132165465454632131321311
DATABASE_URL=postgresql://docmost:STRONG_DB_PASSWORD@db:5432/docmost?schema=public
REDIS_URL=redis://redis:6379
DOCMOST_PORT=5010

#db Configuration
POSTGRES_DB=docmost
POSTGRES_USER=docmost
POSTGRES_PASSWORD=STRONG_DB_PASSWORD

# invite-manager Configuration
DB_HOST=db
DB_PORT=5432

# Docmost Configuration
DOCMOST_URL=http://192.168.1.92:${DOCMOST_PORT}
```

#### Build and Bring Up Stack

You can use the ./restart.sh sctipt or run these comands manually

```
docker compose build 
```

Build Output:

```
docker compose build 
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
[+] Building 0.9s (15/15) FINISHED                                                                                                                                                                                                                                                                 docker:default
 => [invite-manager internal] load build definition from Dockerfile                                                                                                                                                                                                                                          0.0s
 => => transferring dockerfile: 527B                                                                                                                                                                                                                                                                         0.0s
 => [invite-manager internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                                                                                                                           0.8s
 => [invite-manager internal] load .dockerignore                                                                                                                                                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                                              0.0s
 => [invite-manager 1/9] FROM docker.io/library/python:3.11-slim@sha256:614c8691ab74150465ec9123378cd4dde7a6e57be9e558c3108df40664667a4c                                                                                                                                                                     0.0s
 => [invite-manager internal] load build context                                                                                                                                                                                                                                                             0.0s
 => => transferring context: 184B                                                                                                                                                                                                                                                                            0.0s
 => CACHED [invite-manager 2/9] WORKDIR /app                                                                                                                                                                                                                                                                 0.0s
 => CACHED [invite-manager 3/9] RUN pip install psycopg2-binary                                                                                                                                                                                                                                              0.0s
 => CACHED [invite-manager 4/9] COPY invite_script.py .                                                                                                                                                                                                                                                      0.0s
 => CACHED [invite-manager 5/9] COPY create_invites.py .                                                                                                                                                                                                                                                     0.0s
 => CACHED [invite-manager 6/9] COPY invites.csv .                                                                                                                                                                                                                                                           0.0s
 => CACHED [invite-manager 7/9] COPY run_create_invites.sh .                                                                                                                                                                                                                                                 0.0s
 => CACHED [invite-manager 8/9] COPY run_list_invites.sh .                                                                                                                                                                                                                                                   0.0s
 => CACHED [invite-manager 9/9] RUN chmod +x /app/run_create_invites.sh /app/run_list_invites.sh                                                                                                                                                                                                             0.0s
 => [invite-manager] exporting to image                                                                                                                                                                                                                                                                      0.0s
 => => exporting layers                                                                                                                                                                                                                                                                                      0.0s
 => => writing image sha256:2386736611199b6159e30425fd5776d81c62bf5c83cf3edacaab5343833a4794                                                                                                                                                                                                                 0.0s
 => => naming to docker.io/library/docmostinvitelist-invite-manager                                                                                                                                                                                                                                          0.0s
 => [invite-manager] resolving provenance for metadata file                                                                                                                                                                                                                                                  0.0s
[+] Building 1/1
 ✔ invite-manager  Built                                      
```

#### Bring up the stack:

```
docker compose up -d
[+] Running 39/39
 ✔ db Pulled                                                                                                                                                                                                                                                                                                 9.1s 
 ✔ redis Pulled                                                                                                                                                                                                                                                                                             10.2s 
 ✔ docmost Pulled                                                                                                                                                                                                                                                                                           24.8s 
                                                                                                                                                                                                                                                                                                         
[+] Running 8/8
 ✔ Network docmostinvitelist_default             Created                                                                                                                                                                                                                                                     0.0s 
 ✔ Volume "docmostinvitelist_redis_data"         Created                                                                                                                                                                                                                                                     0.0s 
 ✔ Volume "docmostinvitelist_docmost"            Created                                                                                                                                                                                                                                                     0.0s 
 ✔ Volume "docmostinvitelist_db_data"            Created                                                                                                                                                                                                                                                     0.0s 
 ✔ Container docmostinvitelist-db-1              Started                                                                                                                                                                                                                                                     0.6s 
 ✔ Container docmostinvitelist-redis-1           Started                                                                                                                                                                                                                                                     0.7s 
 ✔ Container docmostinvitelist-invite-manager-1  Started                                                                                                                                                                                                                                                     0.5s 
 ✔ Container docmostinvitelist-docmost-1         Started   
```

#### Open the UI:

1. Worksapce: TestWorkspace
2. Enter Name Test Admin
3. Set email <myadmin@test.com>
4. Password: whatever you like

#### Create Invites from a CSV file

Creating invites via the UI is fine, however, you may want to bulk create users from a CSV file

##### CSV Fields:

- email: email youd like to invite
- role: member/admin
- workspace\_name: workspace name ( needs to exist, its looked up for the invite)

Example:

```
email,role,workspace_name,inviter_email
john.doe@example.com,member,TestWorkspace,myadmin@test.com
alice.wonderland@example.com,admin,TestWorkspace,myadmin@test.com
```

##### Execute the script to create invites from the csv filer

```
 docker compose run --rm invite-manager /app/run_create_invites.sh
```

Output:

```
 docker compose run --rm invite-manager /app/run_create_invites.sh
[+] Creating 1/1
 ✔ Container docmostinvitelist-db-1  Running                                                                                                                                                                                                                                                                 0.0s 
Running create_invites.py...
Created invite for john.doe@example.com in workspace 'TestWorkspace' (Inviter: myadmin@test.com).
Created invite for alice.wonderland@example.com in workspace 'TestWorkspace' (Inviter: myadmin@test.com).
Bulk invite creation complete
```

<p class="callout info">Note: If you update the CSV file, you will need to rebuild the container to copy the file over</p>

```
docker compose build
```

Output:

```
docker compose run --rm invite-manager /app/run_create_invites.sh
[+] Creating 1/1
 ✔ Container docmostinvitelist-db-1  Running                                                                                                                                                                                                                                                                 0.0s 
Running create_invites.py...
Created invite for john.doe@example.com in workspace 'TestWorkspace' (Inviter: myadmin@test.com).
Created invite for alice.wonderland@example.com in workspace 'TestWorkspace' (Inviter: myadmin@test.com).
Bulk invite creation complete.
```

#### List Invites

Now you can list the invites and share the links with users as needed

```
sudo docker compose run --rm invite-manager /app/run_list_invites.sh
```

output:

```bash
udo docker compose run --rm invite-manager /app/run_list_invites.sh
[+] Creating 1/1
 ✔ Container docmostinvitelist-db-1  Running                                                                                                                                                                                                                                                                 0.0s 
Running invite_script.py...

Workspace Invitations:
john.doe@example.com: http://192.168.1.92:5010/invites/b9b50c7d-0f37-40e1-b1ef-05bd28b175ce?token=dacfa8a896d14e2d
alice.wonderland@example.com: http://192.168.1.92:5010/invites/252d2739-324a-492f-b8ee-45b0f7c0e847?token=fca83e2c0a184715
```