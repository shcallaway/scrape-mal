#!/bin/bash

DIR="tmp"
rm -rf $DIR
cp -R lambda $DIR

# psycopg2
git clone https://github.com/jkehler/awslambda-psycopg2.git $DIR/awslambda-psycopg2
mv $DIR/awslambda-psycopg2/psycopg2-3.6 $DIR/psycopg2
rm -rf $DIR/awslambda-psycopg2

./venv/bin/pip3 install bs4 -t $DIR
npm i --prefix=$DIR cheerio aws-sdk

zip -r scrape_mal.zip $DIR/*
rm -rf $DIR
