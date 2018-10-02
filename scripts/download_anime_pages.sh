#!/bin/bash

API="https://bj1475vt9h.execute-api.us-east-1.amazonaws.com/default/downloadAnimePages"
COUNTER=0

while [  $COUNTER -lt 500 ]; do
    echo $COUNTER
    curl -H "x-api-key: $API_KEY" -H "content-type: application/json" -d "{ \"pageId\": \"$COUNTER\" }" $API
    let COUNTER=COUNTER+1 
    sleep 1
done
