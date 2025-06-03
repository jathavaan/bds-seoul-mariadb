# BDS Seoul MariaDB

## Setup

### Local setup

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

### Raspberry Pi setup

We use `envsubst` to inject the correct IP-addresses when building the docker images. The IP-addresses are set in
`~/.zshrc`. To set the IP-addresses, you can use `nano ~/.zshrc` and add the following lines:

```bash
export SEOUL_1_IP=<ip-address-of-seoul-1-raspberry-pi>
export SEOUL_2_IP=<ip-address-of-seoul-2-raspberry-pi>
export SEOUL_3_IP=<ip-address-of-seoul-3-raspberry-pi>
export SEOUL_4_IP=<ip-address-of-seoul-4-raspberry-pi>
```

Press `CTRL + X`, then `Y` and `Enter` to save the file. After that, run `source ~/.zshrc` to apply the changes. You
have now set the IP-addresses for the Raspberry Pis, and you only need to do this if the IP-addresses of any Raspberry
Pi changes.

Using `envsubst`, you can now configure the correct `.env` file. Simply run the following command in the root of
`bds-seoul-mariadb` directory:

```bash
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. The docker images are now ready to
be built. Build and start the containers and force recreating with the following command:

```bash
sudo docker compose up -d --force-recreate
```

To view the logs of the containers, you can use the following command:

```bash
sudo docker logs -f <container-name>
```