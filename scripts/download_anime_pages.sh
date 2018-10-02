#!/bin/bash

API="https://bj1475vt9h.execute-api.us-east-1.amazonaws.com/default/downloadAnimePages"
COUNT=${COUNT:-0}

while [  $COUNT -lt 500 ]; do
    curl -H "x-api-key: $API_KEY" -H "content-type: application/json" -d "{ \"pageId\": \"$COUNT\" }" $API
    echo "pageId=$COUNT"
    let COUNT=COUNT+1
    sleep 60
done
