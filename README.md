# aws-sam-s3-dynamodb

The serverless application that uses Rekognition APIs to detect text in S3 Objects and stores labels in DynamoDB using AWS SAM.

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

## Before deploying the sample application

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

## Getting started with the SAM Template

- To build and deploy your application at the beginning, run the following commands:

  - Use a sam package command when you upload lambda functions zip files to S3

```bash
# Create S3 bucket
s3 mb s3://<bucket-name>

# Output the template file via S3 which uploaded lambda function resources on
sam package \
 --template-file template.yaml \
 --output-template-file package.yaml \
 --s3-bucket <bucket-name>

# Deploy
sam deploy \
 --template-file package.yaml \
 --stack-name aws-sam-s3-dynamodb \
 --capabilities CAPABILITY_IAM
```
 Cloudformation and Lambda function, DynamoDB will be created After deployed.


## Deploy sam from the initial

- Create a template for sam if you want to start with your own serverless application
  ```bash
  sam init --runtime python3.8
  sam build
  sam deploy --guided
  ```


## Check if the rekognition API is succeeded
Upload an image file as using it for lambda function
```bash
# check S3 bucket name after deploying on S3.
aws s3 ls
aws s3api put-object --bucket aws-sam-s3-dynamodb-xxxxxxxx --key upload_image.jpeg --body resources/gratisography-hot-wash-800x525.jpg

# Call the lambda function
aws lambda invoke  --function-name aws-sam-s3-dynamodb-DetectTextInImageFunction-xxxxxxxx --invocation-type Event output.json

# You can see a record on DynamoDB and the upload_image.jpeg on S3 bucket.
aws dynamodb scan --table-name aws-sam-s3-dynamodb-ResultsTable-xxxxxxxxx
```


## Cleanup

To delete the sample application that you created, use the AWS CLI.
```bash
aws cloudformation delete-stack --stack-name aws-sam-s3-dynamodb
# aws cloudformation delete-stack --stack-name aws-sam-s3-dynamodb --region ap-northeast-1
```

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests.

```bash
pip install pytest pytest-mock --user
python -m pytest tests/ -v
```
