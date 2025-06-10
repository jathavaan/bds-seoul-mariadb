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

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
    - [Local setup](#local-setup)
    - [Raspberry Pi setup](#raspberry-pi-setup)
    - [Starting the services](#starting-the-services)
    - [Applying migrations](#applying-migrations)

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

### Raspberry Pi setup

The Raspberry Pi setup is more complex and requires multiple Raspberry Pis to be set up. The first step is to identify
the IP-addresses of the Raspberry Pis. Open a terminal on your computer and ssh into the Raspberry Pi:

```powershell
ssh seoul-2@<ip-address-of-raspberry-pi-2>
```

Replace `<ip-address-of-raspberry-pi-2>` with the actual IP-address of the Raspberry Pi, and enter the password
`seoul-2`.

Then change directory into the `bds-seoul-mariadb` directory:

```powershell
cd bds-seoul-mariadb
```

We use `envsubst` to inject the correct IP-addresses when building the docker images. The IP-addresses are set in
`~/.zshrc`. To set the IP-addresses, you can use `nano ~/.zshrc` and add the following lines:

```powershell
export SEOUL_1_IP=<ip-address-of-seoul-1-raspberry-pi>
export SEOUL_2_IP=<ip-address-of-seoul-2-raspberry-pi>
export SEOUL_3_IP=<ip-address-of-seoul-3-raspberry-pi>
export SEOUL_4_IP=<ip-address-of-seoul-4-raspberry-pi>
```

Press `CTRL + X`, then `Y` and `Enter` to save the file. After that, run

```bash
source ~/.zshrc
``` 

to apply the changes. You
have now set the IP-addresses for the Raspberry Pis, and you only need to do this if the IP-addresses of any Raspberry
Pi changes.

Using `envsubst`, you can now configure the correct `.env` file. Simply run the following command in the root of
`bds-seoul-mariadb` directory:

```powershell
envsubst < .env.template > .env
```

This will create a `.env` file with the correct IP-addresses for the Raspberry Pis. Run

```powershell
cat .env
```

to verify that the environment variables are set correctly.

### Starting the services

> [!NOTE]
> If you are running the project on Raspberry Pis, use `sudo docker compose` instead of `docker-compose`.

> [!WARNING]
> Log into Docker CLI before proceeding to the next steps. The processs will fail otherwise. Please read [the Docker documentation](https://docs.docker.com/reference/cli/docker/login/) to learn how to do it.

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

And then wait another 30~60 seconds before starting the database-script container:

```powershell
docker-compose up -d database-script
```

To make sure that everything is running correctly, you can check the logs of the containers with the following command:

```powershell
docker-compose logs -f database-script
```

If an error occurs, simply restart the `database-script` container with the following command:

```powershell
docker-compose restart database-script
```

At this point the database-script logs should look something like this:

```plaintext
2025-06-09T03:01:40.609321423Z [INFO] 2025-06-09 03:01:39 application.services.kafka_service.kafka_service:18            KafkaService initialized and attempting to clear topics
2025-06-09T03:01:40.609321423Z [INFO] 2025-06-09 03:01:40 application.services.kafka_service.kafka_service:39            Deleted topic 'reviews'
2025-06-09T03:01:40.631393211Z [INFO] 2025-06-09 03:01:40 application.services.kafka_service.kafka_service:39            Deleted topic 'mapreduce_results'
2025-06-09T03:01:40.945278747Z [INFO] 2025-06-09 03:01:40 application.services.kafka_service.kafka_service:39            Deleted topic 'final_results'
2025-06-09T03:01:40.970880351Z [INFO] 2025-06-09 03:01:40 application.services.kafka_service.kafka_service:39            Deleted topic 'last_scraped_date_requests'
2025-06-09T03:01:41.424629283Z [INFO] 2025-06-09 03:01:41 application.services.kafka_service.kafka_service:39            Deleted topic 'last_scraped_date_responses'
2025-06-09T03:01:41.444638334Z [INFO] 2025-06-09 03:01:41 application.services.kafka_service.kafka_service:39            Deleted topic 'process_status'
2025-06-09T03:01:43.527747464Z [INFO] 2025-06-09 03:01:43 application.services.kafka_service.kafka_service:49            Attempting to re-create topics
2025-06-09T03:01:44.061270962Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'reviews'
2025-06-09T03:01:44.064693487Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'mapreduce_results'
2025-06-09T03:01:44.068665100Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'final_results'
2025-06-09T03:01:44.111385181Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'last_scraped_date_requests'
2025-06-09T03:01:44.115569145Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'last_scraped_date_responses'
2025-06-09T03:01:44.156144931Z [INFO] 2025-06-09 03:01:44 application.services.kafka_service.kafka_service:63            Created topic 'process_status'
2025-06-09T03:01:44.159998659Z [INFO] 2025-06-09 03:01:44 application.container:18                                       Waiting 10 seconds while waiting for the database container
2025-06-09T03:01:54.333557637Z [INFO] 2025-06-09 03:01:54 entrypoints.consumers.last_scraped_date_consumer:42            Kafka Consumer connected to bootstrap server [host.docker.internal:9092] with group ID seoul, subscribed to topic(s): last_scraped_date_requests
2025-06-09T03:01:54.347340767Z [INFO] 2025-06-09 03:01:54 entrypoints.consumers.mapreduce_result_consumer:46             Kafka Consumer connected to bootstrap server [host.docker.internal:9092] with group ID seoul, subscribed to topic(s): mapreduce_results
```

To exit the log view please press `CTRL + C`.

If it's your first time running the project you have to apply migrations to the database. See
the [Applying migrations](#applying-migrations) section for more information. If the previous steps are successful, the
Hadoop repository can be started. Check the [Hadoop repository](https://github.com/jathavaan/bds-seoul-hadoop) for more
information on how to set it up.

### Applying migrations

> [!NOTE]
> Make sure to activate the virtual environment before applying the migrations if you are using one.

If you're configuring the project locally, you first have to change the `DB_HOST` in the `.env` file to `localhost`.
Then in the root of the `bds-seoul-mariadb` directory, run the following command to apply the migrations:

```powershell
alembic upgrade head
```

Remember to change the `DB_HOST` back to `host.docker.internal` after applying the migrations. To apply the migrations
on the Raspberry Pis set the `DB_HOST` in the `.env` file to the IP-address of the second Raspberry Pi on the rack (
`seoul-2`) and run the same command as above. Restart the `database-script` container after applying the migrations:

```powershell
docker-compose restart database-script
```
