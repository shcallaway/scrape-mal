#!/bin/bash

COUNT=${COUNT:-0}

while [  $COUNT -lt 500 ]; do
    echo "mal_id: $COUNT"
    curl -H "x-api-key: $API_KEY" -H "content-type: application/json" -d "{ \"mal_id\": \"$COUNT\" }" $API_URL
    let COUNT=COUNT+1
    sleep 60
done
