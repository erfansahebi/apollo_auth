# Apollo

RSS Project with microservice architecture.

## Overview

Nameko is a Python microservices framework that helps developers create and manage microservices-based applications.
It simplifies communication between microservices and handles dependencies.
Nameko is built on RabbitMQ, a message broker, and supports features like RPC calls and event-driven communication.
It's designed for building distributed, scalable, and easily testable applications.
You can use Nameko with web frameworks like Flask and Django, and it offers extensibility for custom functionality.

It's a great choice for Python developers looking to embrace microservices.
Microservices with API Gateway which handles incoming HTTP requests.
data of HTTP requests will be forwarded to these Microservices by <b>RPC</b>.
Additionally, we deal with Authentication, Redis and PostgreSQL.

## Architecture

Microservice architecture is an architectural style that structures an application as a collection of small, loosely
coupled, and independently deployable services.
In this architecture, each service represents a specific business capability and can be developed, deployed, and scaled
independently.
Services communicate with each other through well-defined APIs, typically over lightweight protocols like HTTP or
messaging queues.

RPC (Remote Procedure Call) is a way for programs to request and execute functions or procedures on remote computers
over a network.
It's language-agnostic and typically synchronous.
Developers use stubs or proxies to make these remote calls.
RPC handles data serialization, error handling, and can use various transport protocols.
Security is important in RPC.
It simplifies building distributed systems but requires careful design for error handling and versioning.
Popular RPC frameworks include gRPC and Apache Thrift.

## Prerequisites

- Git
- Docker

## Getting Started

Repositories:

- [Apollo EnvDev](https://github.com/erfansahebi/apollo_envdev) ( Docker )
- [Apollo Gateway](https://github.com/erfansahebi/apollo_gateway)  ( Python -> Nameko )
- [Apollo Auth](https://github.com/erfansahebi/apollo_auth) ( Python -> Nameko )
- [Apollo Rss](https://github.com/erfansahebi/apollo_rss) ( Python -> Nameko )
- [Apollo Shared](https://github.com/erfansahebi/apollo_shared) ( Python -> Package)

<hr>

### 1. Install git

 ```shell
sudo apt install git-all
```

### 2. Pull [Apollo EnvDev](https://github.com/erfansahebi/apollo_envdev)

```shell
git pull https://github.com/erfansahebi/apollo_envdev.git
```

In this repo, we have a shell for pulling all Repositories.

### 3. Pull all Repositories:

```shell
chmod +x build.sh
```

```shell
sh build.sh
```

### 4. Make Docker Images

```shell
make build
```

### 5. Set Environments

```shell
cp .env.example .env
```

### 6. run Docker:

```shell
dokcer compose up --build -d
```