# Lambda-Docker
Simple webapp using AWS Lambda, API Gateway and Docker.

## Change code, then build image
docker build -t python-containers .

## Tag new image
docker tag python-containers:latest 691342082863.dkr.ecr.us-east-1.amazonaws.com/python-containers:latest

## Push to ECR in AWS
docker push 691342082863.dkr.ecr.us-east-1.amazonaws.com/python-containers:latest

## Deploy
Create Lambda function or change image to the recently uploaded one.
