# DEX Integration Project Documentation

This documentation provides a guide on setting up the DEX Integration project using Docker, including configuration files and running the Docker container. Additionally, it outlines how to log in to the Docker container and execute the test.py script for testing purposes.

## Setup Instructions

Follow the steps below to set up and run the DEX Integration project:

1. Clone the Repository
   Clone the DEX Integration repository from the provided location:

```
https://github.com/digitalsimboja/DEX
```

2. Navigate to the Project Directory

Change your current directory to the root directory of the cloned repository:

```
cd DEX
```

3. Docker Setup
   There is a `docker-compose.yml` and `Dockerfile` for setting up the `Hyperliquid` client.
   Before you build the docker containers, you must add the appropriate config files

4. Configuration Files
   Redis Configuration

Create a Redis configuration file named redis_config.json with the following content:

```
{
  "host": "redis",
  "port": 6379,
  "db": 0
}
```

    Hyperliquid configuration

Dockerfile is provided at `adapters/hyperliquid/Dockerfile`
Create the hyperliquid_config.json with the following content:

```
{
    "base_url": "https://api.hyperliquid.xyz/info",
    "websocket_url": "wss://api.hyperliquid.xyz/ws",
    "endpoints": {
        "allMids": ""
    }
}
```

    Global configuration

Create a `config.json` file and add the following contents:

```
{
    "api_key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
    "api_qps": 5
}
```

The above configuration are not to be used for production

5. Building and Running Docker Container
   Build the Docker container using the provided Dockerfile:

```
docker compose up -d --build
```

6. Run the docker container
   Login to the docker container built with the image name `contractor_case_study-main-hyperliquid-marketdata-adapter-1` using the `CONTAINER ID` created

```
docker exec -it <CONTAINER_ID> /bin/bash
```

7. Executing the Test Script
   After logging in to the Docker container, you can execute the test.py script as follows:

```

python test.py

```

Wait for about 20 seconds for the script to complete its execution.

8. Repeat Execution
   After the initial execution, you can run the test.py script again to consume the data after a short interval:

```

python test.py

```
