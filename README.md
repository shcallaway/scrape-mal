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

## Production

scrape_mal is deployed in production using AWS Lambda (as an HTTP API), S3 (for storing raw HTML), and Postgres on RDS.
