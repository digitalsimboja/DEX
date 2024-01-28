# Case Study - DEX Integration

## Introduction

Follow this integration guide to properly integrate a DEX into our codebase. The integration is divided into three sprints: (i) Integrating the API endpoints / websocket, (ii) adapting raw data from redis and publishing adapted responses, (iii) building a client to easily fetch the adapted responses from redis.

In your local environment, you will need Python 3.10 and Docker (pulling a redis image) to run code. Be ready to generate json configs during the development process. Further details are provided in the documentation below.

## Case Study Instructions
In this case study, you are asked to integrate the Hyperliquid decentralized exchange using our internal standards. Abstract classes and utility functions have already been built for you to streamline the integration. The ask is for a single endpoint to be integrated from Hyperliquid's API: [**Retrieve all mids for all actively traded coins**](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) on the url https://api.hyperliquid.xyz/info. If you can integrate this endpoint into the Hyperspace client, publish the raw response to Redis,  adapt the raw response, and consume the adapted response, the case study will successfuly be completed.

Perform the integration following the three parts below.


## Part 1. Integrating APIs

### Overview

DEX exchanges will expose REST-based, GraphQL-based, or Websocket-based resources. This step will result in a client to hit any necessary resource for raw responses and publish these raw responses as JSON strings to Redis. Refer to the `DataConsumer` object’s abstract methods inside **data_client/data_client.py** module for examples of the types of data to be integrated.

### API Integration

1. Refer to the **api** directory in the project repository.
2. Create a new sub-directory named after the exchange being integrated inside the api.
3. Use the **dex_exchange_base.py** module as a template for building the client.
4. Ask for API keys and proper API documentation from us for integration.
5. Store exchange-specific modules in the sub-directory to avoid confusion.
6. Follow the existing hyperliquid example for guidance.
7. Provide a Redis config JSON file for the `RedisStreamManager`.

### Client Architecture

Refer to the [Generic DEX Client](https://github.com/gpresearch/contractor_case_study/blob/main/generic%20dex%20client) for the general structure.


## Part 2. Adaptors

### Overview

Once the client is able to read data and publish to Redis, build an adaptor to adapt raw data into a standard format. Adaptors will run as jobs listening to Redis for any new raw data received from the client.

1. Look at the **adapters** directory and the **dex_adaptor_base.py** module.
2. Code the adaptors, saving each exchange to a sub-directory.
3. Do not delete the raw data from Redis; keep it available for other internal systems.

## Part 3. DataConsumer

The final portion is building the `DataConsumer` in the **data_client** directory.

1. Create a sub-directory for the exchange being integrated.
2. Place the newly created client in this sub-directory.
3. This is simple fetching with no data manipulation.
4. Access adapted data easily from anywhere in our codebase.

If a client needs source or timestamp information, it will be available inside the Redis stream.
