# bds-seoul-2

`.env` file

Select `DB_HOST=localhost` when you want to connect to database from your terminal, IDE or generally on your computer,
and `DB_HOST=host.docker.internal` when you build the docker image.

```dotenv
DB_USERNAME="root"
DB_PASSWORD="seoul-2"
#DB_HOST=localhost
DB_HOST=host.docker.internal
DB_PORT="3306"
DB_NAME="seoul-2-db"
KAFKA_BOOTSTRAP_SERVERS=host.docker.internal
SEQ_SERVER=host.docker.internal
SEQ_PORT=5341
```