# docker-database-server
A dockerised, sqlite3 database with a front-end RESTapi written in python, deployed by ansible.

## Set up as a service
>sudo mkdir /opt/database-server  
>sudo nano /etc/systemd/system/database-server.service  

```
[Unit]
Description=Docker Database server application
After=network.target

[Service]
User=pi
WorkingDirectory=/opt/database-server
ExecStart=/usr/bin/python3 /opt/database-server/docker-database-server/app.py
Restart=always

[Install]
WantedBy=multi-user.target

```

> sudo systemctl daemon-reload  
> sudo systemctl enable database-server  
> sudo systemctl start database-server  
> sudo systemctl status database-server  

### Set up a crontab which checks for changes
If you want the jenkins build (which includes testing) when there is a change in repo, then use this command:
> 0 1 * * * cd /var/lib/jenkins/workspace/test_docker-database-server && [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ] && git fetch origin && curl -X POST http://192.168.1.135:8080/job/docker-database-server --user <insert name>:api token


## Fault finding
> journalctl -u database-server -f  






## Coverage.
> pip install coverage
> python -m coverage run -m unittest
> python -m coverage report
> python -m coverage html

## Pylint
>pip install pylint
File -> Settings -> Tools -> External Tools -> "add"
 - In "Name" put pylint
 - In "Program" put location of and pylint.exe
 - In "Paramaters" put $FilePath$
Tools -> External tools -> pylint

## Development Update
### update 22/08/23. 
> Coverage - "Total	714	314	0	56%"
> Pylint - "Your code has been rated at 5.35/10" - for testing.
> Pylint - "Your code has been rated at 5.11/10" for src.