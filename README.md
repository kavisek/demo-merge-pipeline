# demo-merge-pipeline

This is a demo project to show how to merge data in postgres. The project is a simple python script that merges data from two tables. The script is scheduled to run every minute.

```bash
make start
```

## Overview

- local postgres database
- flyway manages the migrations
- a simple crontab scheduler
- configParser stores the configuration details

## Local Datbase Credentials

host: localhost  
port: 5432  
username: postgres  
password: docker  

# References

- https://hub.docker.com/_/mysql