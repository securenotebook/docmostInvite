# setup

This small docker stack builds on the default docker compose provided by docmost here: [https://raw.githubusercontent.com/docmost/docmost/main/docker-compose.yml](https://raw.githubusercontent.com/docmost/docmost/main/docker-compose.yml)

Note this is af full replacement!

#### Clone the repo

```bash
git clone https://github.com/securenotebook/docmostInvitelist.git
```

#### Setup Envrioment Vars

cd into folder and edit the .env file as needed - Change DOCMOST\_URL to match your setup - everything else can be left as is

```
cd docmostInvitelist
nano .env
```

<span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Oxygen, Ubuntu, Roboto, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400;">build and bring it up the stack</span>

```
sudo docker compose build
sudo docker compose up -d
```

Create invites as you normally would from the UI

You can then run:

```
sudo docker compose run --rm invite-manager
```

output:

```bash
docmostInvitelist$ sudo docker compose run --rm invite-manager
[sudo] password for wes: 
WARN[0000] /home/wes/docmostInvitelist/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Creating 1/1
 ✔ Container docmostinvitelist-db-1  Running                                                                                                                                                                                                                              0.0s 

Workspace Invitations:
test1@testing.com: http://192.168.1.92:5010/invites/01955ab9-1e85-78dd-88b2-d9e6f6fbc7c0?token=e0bkonj8u82f8t5b
test2@admin.com: http://192.168.1.92:5010/invites/01955ab9-62ae-724e-a567-1b169d1ca2d8?token=ymxdm2cps5clq30h
```