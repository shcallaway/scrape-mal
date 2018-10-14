# scrape_mal

:innocent:

I want your data. uwu

## Development

Create a Python virtual environment:

```
make dev && source ./venv/bin/activate
```

To exit the virtual environment, run `deactivate`.

You will need to configure the AWS CLI or provide the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables in order to execute some scripts.

## Deployment

scrape_mal is deployed in production using the following AWS resources:

- Lambda
- API Gateway
- S3
- RDS

`lambda/insert_anime_record.py` must be deployed using a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) because it requires the psycopg2 package. Fortunately, there is a pre-compiled Lambda-compatible version of psycopg2 available [here](https://github.com/jkehler/awslambda-psycopg2). You can get the relevant code with this:

```
git clone https://github.com/jkehler/awslambda-psycopg2.git && \
mv awslambda-psycopg2/psycopg2-3.6 psycopg2 && \
rm -rf awslambda-psycopg2
```

## Todo

- Cloudformation
- [VPC](https://aws.amazon.com/blogs/aws/new-access-resources-in-a-vpc-from-your-lambda-functions/)
- Script for `lambda/insert_anime_record.py` deployment
