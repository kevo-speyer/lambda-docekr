# Lambda-Docker
Simple webapp using AWS Lambda, API Gateway and Docker.

## Define environment variables
```
ecr_name=python-containers
aws_account_id=691342082863
region=us-east-1
```

## Build image
`docker build -t ${ecr_name} .`

## Tag new image
`docker tag ${ecr_name}:latest ${aws_account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_name}:latest`

## Push to ECR in AWS
`docker push ${aws_account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_name}:latest`
### If there is a Failure to authenticate, run:
`aws ecr get-login-password --region $region | docker login --username AWS --password-stdin ${aws_account_id}.dkr.ecr.${region}.amazonaws.com`

## Deploy
* Create Lambda function from container image or change image to the recently uploaded one
* Create Api Gateway to trigger said Lambda

## Request API
```
api_url="https://m71m1d0nr2.execute-api.us-east-1.amazonaws.com"
curl -XGET $api_url -d '{"from":"2020-01-01","to":"2020-05-31"}'
```

# Development Workflow

## Local Lambdas Deploy
`docker run -p 9000:8080  ${ecr_name}:latest`

## Local Lambdas trigger
`curl -XGET "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"from":"2020-01-01","to":"2020-05-31"}'`
