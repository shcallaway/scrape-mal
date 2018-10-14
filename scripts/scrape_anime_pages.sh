#!/bin/bash

COUNT=${COUNT:-1}

while [  $COUNT -lt 500 ]; do
    # echo "pageId=$COUNT"
    python3 ./lib/scrape_anime_page.py $COUNT
    let COUNT=COUNT+1
    sleep 1
done
