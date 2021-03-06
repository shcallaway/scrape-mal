# Scrape MAL

Scrape MAL is an HTTP API for scraping [My Anime List](https://myanimelist.net/) pages. 

## Development

This project is written in both Python and JavaScript. Python because it is easy to get up-and-running in AWS Lambda, and JavaScript because JS is particularly good at parsing HTML.

To develop the Python parts, create a Python virtual environment:

```
make dev && source ./venv/bin/activate
```

To develop the JavaScript parts, simply install the Node modules:

```
npm i
```

Note: You will need to configure the AWS CLI so that you're authenticated with AWS.

### API

- /download - Save an HTML page to S3.
- /extract - Extract data from a page that was previously saved to S3.
- /insert - Insert data into the database.
- /scrape - Combines the extract and insert functions.

All endpoints use HTTP method POST.

## Deployment

SCrape MAL is deployed in production using AWS Lambda, API Gateway, S3 and RDS.

### Lambda

`scripts/create_deployment_package.sh` will create a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) that will work for all of the Lambdas.

### RDS

`lambda/insert.py` requires a Postgres databse on RDS. You can create the main table with this command:

```
CREATE TABLE anime (
    mal_id integer NOT NULL,
    title text NOT NULL,
    alt_title_en text,
    alt_title_jp text,
    type text,
    num_episodes integer,
    status text,
    aired text,
    premiered text,
    broadcast text,
    source text,
    duration text,
    rating text,
    synopsis text,
    background text
);
```

## Todo

- Infrastructure as Code (CloudFormation or Terraform)
- [VPC](https://aws.amazon.com/blogs/aws/new-access-resources-in-a-vpc-from-your-lambda-functions/)
