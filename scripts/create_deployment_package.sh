#!/bin/bash

DIRECTORY="tmp"
ZIPFILE="scrape_mal.zip"

rm -rf $ZIPFILE $DIRECTORY
mkdir $DIRECTORY

cp -R lambda/* $DIRECTORY

chmod u=rwx,g=rx,o=rx $DIRECTORY/*.js
chmod u=rwx,g=rx,o=rx $DIRECTORY/*.py

# psycopg2
git clone https://github.com/jkehler/awslambda-psycopg2.git $DIRECTORY/awslambda-psycopg2
mv $DIRECTORY/awslambda-psycopg2/psycopg2-3.6 $DIRECTORY/psycopg2
rm -rf $DIRECTORY/awslambda-psycopg2

# bs4
./venv/bin/pip3 install bs4 -t $DIRECTORY

# node_modules
npm i --prefix=$DIRECTORY cheerio aws-sdk

cd $DIRECTORY
zip -r ../$ZIPFILE *
cd ..

rm -rf $DIRECTORY
