#!/bin/bash

if [ -z "$URL" ] || [ -z "$API_KEY" ]; then
    echo "URL or API_KEY is missing."
    exit 1
fi

START=${START:-0}
MAX=${MAX:-500}
INTERVAL=${INTERVAL:-1}

echo "URL=$URL"
echo "START=$START"
echo "MAX=$MAX"
echo "INTERVAL=$INTERVAL"

COUNT=$START

while [  $COUNT -lt $MAX ]; do
    echo "mal_id: $COUNT"
    curl -H "x-api-key: $API_KEY" -H "content-type: application/json" -d "{ \"mal_id\": \"$COUNT\" }" $URL
    let COUNT=COUNT+1
    sleep $INTERVAL
done
