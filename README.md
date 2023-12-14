# Filenne Services Infrastructure

This repository contains the configuration and scripts necessary to manage the infrastructure for Filenne services. It includes a Makefile for local development and a `serverless.yml` for AWS Lambda deployment.

## Makefile Overview

The Makefile is designed to facilitate the development, testing, and deployment of Filenne services. It includes several commands:

- `info`: Displays information about the main repository.
- `help`: Lists available make commands with descriptions.
- `install`: Sets up a virtual environment and installs necessary dependencies.
- `user-api`: Activates the virtual environment and sets up the user API service.
- `api`: Similar to `user-api`, but sets up the general API service.
- `user-api-local` and `api-local`: Install dependencies and start respective local services.
- `local`: Starts both user and general API services locally.

## Serverless.yml Overview

The `serverless.yml` file defines the configuration for deploying services on AWS using the Serverless Framework. Key aspects:

- **Service and App Name**: Identified as `filenne-infrastructure`.
- **Framework Version**: Specifies the Serverless Framework version used.
- **Provider**: AWS Lambda with specific configurations like region, stage, and IAM roles.
- **Functions**: Defines two Lambda functions (`user-api` and `api`) with their specific configurations such as memory size, timeout, runtime, and environmental variables.
- **Layers**: Includes two layers, `fastapiAuthorizer` and `fastapi`, which contain dependencies for the Lambda functions.
- **Resources**: References to additional AWS resources required by the services, such as IAM roles, DynamoDB tables, and S3 buckets.
- **Custom Configurations**: Defines custom variables like resource bucket names and environment-specific settings.

## Getting Started

1. **Prerequisites**:
   - Python 3
   - AWS CLI
   - Serverless Framework

2. **Local Setup**:
   - Clone the repository.
   - Run `make install` to set up the virtual environment and install dependencies.

3. **Using Makefile**:
   - Use `make help` to see available commands.
   - Use `make local` to start local development servers.

4. **Deployment**:
   - Configure AWS credentials.
   - Deploy using `serverless deploy --stage [dev|stg|prd]`.

## Contribution Guidelines

Contributors are welcome to propose changes or improvements to the infrastructure. Please adhere to the existing coding and commit message standards.
