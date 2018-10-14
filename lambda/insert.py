import json
import psycopg2
import os


def respond_with(status_code):
    return {
        "statusCode": status_code
    }


def create_sql_statement(data):
    keys = data.keys()

    columns = ", ".join(keys)
    values = ", ".join(list(map(lambda key: f"%({key})s", keys)))

    return f"INSERT INTO anime ({columns}) VALUES ({values})"


def get_pg_connection():
    return psycopg2.connect(
        host=os.environ["PG_HOST"],
        user=os.environ["PG_USERNAME"],
        password=os.environ["PG_PASSWORD"],
        dbname=os.environ["PG_DATABASE"]
    )


def lambda_handler(event, context):
    print(f"Event: {event}")

    data = None

    try:
        data = json.loads(event["body"])
    except Exception as error:
        print(error)
        return respond_with(400)

    print("Connecting to Postgres.")

    connection = get_pg_connection()
    cursor = connection.cursor()

    statement = create_sql_statement(data)
    print(f"Executing: {statement}")
    cursor.execute(statement, data)

    connection.commit()

    cursor.close()
    connection.close()

    return respond_with(201)
