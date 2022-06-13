# Lambda-Docker
Simple webapp using AWS Lambda, API Gateway and Docker.

## Define environment variables
```
ecr_name=python-containers
aws_account_id=691342082863
region=us-east-1
```

## Change code, then build image
`docker build -t ${ecr_name} .`

## Tag new image
`docker tag ${ecr_name}:latest ${aws_account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_name}:latest`

## Push to ECR in AWS
`docker push ${aws_account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_name}:latest`

## Deploy
Create Lambda function or change image to the recently uploaded one

## Local Lambda Test 

### Local Lambdas Deploy
`docker run -p 9000:8080  ${ecr_name}:latest` 

### Local Lambdas trigger
`curl -XGET "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"from":"2020-01-01","to":"2020-05-31"}'`

