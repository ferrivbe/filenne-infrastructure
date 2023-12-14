.DEFAULT_GOAL := help

include .env

.PHONY: info
info:
	@echo "This is the main repository for Filenne services infrastructure."

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install:
	@python3 -m pip install virtualenv\
		&& python3 -m virtualenv venv\
		&& . venv/bin/activate\
		&& python3 -m pip install -r functions/user-api/src/requirements.txt\
		&& python3 -m pip install -r functions/user-api/src/requirements.local.txt

.PHONY: user-api
user-api:
	@. venv/bin/activate\
		&& export CLIENT_ID="${CLIENT_ID}"\
		&& export CLIENT_SECRET="${CLIENT_SECRET}"\
		&& export REGION="${REGION}"\
		&& export SERVICE_ENVIRONMENT="${SERVICE_ENVIRONMENT}"\
		&& export USERPOOL_ID="${USERPOOL_ID}"\
		&& cd functions/user-api/src\
		&& python3 -m uvicorn handler:app --reload --port 8000

.PHONY: api
api:
	@. venv/bin/activate\
		&& export FILES_BUCKET_NAME=${FILES_BUCKET_NAME}\
		&& export FILE_SERVICE_BASE_URL=${FILE_SERVICE_BASE_URL}\
		&& export CLOUDFRONT_PRIVATE_KEY="${CLOUDFRONT_PRIVATE_KEY}"\
		&& export CLOUDFRONT_PUBLIC_KEY_ID=${CLOUDFRONT_PUBLIC_KEY_ID}\
		&& cd functions/api/src\
		&& python3 -m uvicorn handler:app --reload --port 8002

.PHONY: user-api-local
user-api-local: install user-api

.PHONY: api-local
api-local: install api

.PHONY: local
local: user-api-local api-local
