# Big Data Systems Team Seoul - MariaDB, Kafka and Seq

This repository contains the code for the Big Data Systems course project, which involves setting up a MariaDB database,
a Kafka message broker, and a Seq log server. The project is designed to run on multiple Raspberry Pi devices, with each
device running a different component of the system. The project is built using Docker and Docker Compose, allowing for
easy deployment and management of the services.

> [!NOTE]
> To correctly run the project, you need to start this repository first, then the two other repositories. This is the
> correct order:
>  1. [bds-seoul-mariadb](https://github.com/jathavaan/bds-seoul-mariadb)
>  2. [bds-seoul-hadoop](https://github.com/jathavaan/bds-seoul-hadoop)
>  3. [bds-seoul-client](https://github.com/jathavaan/bds-seoul-client)

## Table of Contents

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)

## Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/jathavaan/bds-seoul-mariadb.git
   ```

2. Navigate to the project directory:

   ```powershell
    cd bds-seoul-mariadb
    ```
3. Create a virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   ```

4. Activate the virtual environment. On Windows:
   ```powershell
    venv\Scripts\activate
    ```
   On macOS/Linux:
    ```powershell
    source venv/bin/activate
    ```

5. Install the required Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

## Setup

There are two different setups for this project: one for local development and one for running on Raspberry Pis. The
Raspberry Pi setup takes a considerable amount of time to set up, so it is recommended to use the local setup. The
functionality is the same, just faster and more stable locally.

### Local setup

The first step of local setup is to create a `.env` file in the root of the `bds-seoul-mariadb` directory. Paste the
following into `.env`

```dotenv
DB_USERNAME="root"
DB_PASSWORD="seoul-2"
DB_HOST=host.docker.internal
DB_PORT="3306"
DB_NAME="seoul-2-db"
KAFKA_BOOTSTRAP_SERVERS=host.docker.internal
SEQ_SERVER=host.docker.internal
SEQ_PORT=5341
```

The next step is to create the containers by running the following command in the root of `bds-seoul-mariadb` directory:

```powershell
docker-compose up -d seq zookeeper mariadb
```

Ensure that Zookeeper is running before starting the Kafka container. You can check the logs of Zookeeper with the
command

```powershell
docker-compose logs -f zookeeper
```

Make sure to wait 30~60 seconds after starting Zookeeper before starting the Kafka container. You can start the Kafka
container with the following command:

```powershell
docker-compose up -d kafka
```

And then wait another 30~60 seconds before starting the python script container:

```powershell
docker-compose up -d python-script
```

To make sure that everything is running correctly, you can check the logs of the containers with the following command:

```powershell
docker-compose logs -f database-script
```

If an error occurs, simply restart the `database-script` container with the following command:

```powershell
docker-compose restart database-script
```

Select `DB_HOST=localhost` when you want to connect to database from your terminal, IDE or generally on your computer,
and `DB_HOST=host.docker.internal` when you build the docker image.

### Raspberry Pi setup

We use `envsubst` to inject the correct IP-addresses when building the docker images. The IP-addresses are set in
`~/.zshrc`. To set the IP-addresses, you can use `nano ~/.zshrc` and add the following lines:

```powershell
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

```powershell
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. The docker images are now ready to
be built. Build and start the containers and force recreating with the following command:

```powershell
sudo docker compose up -d --force-recreate
```

To view the logs of the containers, you can use the following command:

```powershell
sudo docker logs -f <container-name>
```