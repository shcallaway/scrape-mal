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

### Lambda

`./scripts/create_deployment_packages.sh` will create a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) for each of the Lambdas.

### RDS

`insert.py` requires a Postgres databse on RDS. You can create the main table with this command:

```
CREATE TABLE anime (
    mal_id integer NOT NULL,
    title varchar(120) NOT NULL,
    alt_title_en varchar(120),
    alt_title_jp varchar(120)
);
```

## Todo

- Cloudformation
- [VPC](https://aws.amazon.com/blogs/aws/new-access-resources-in-a-vpc-from-your-lambda-functions/)
