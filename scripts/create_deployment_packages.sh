#!/bin/bash

DIR="deploy"

rm -rf $DIR

mkdir $DIR
mkdir $DIR/extract
mkdir $DIR/insert

cp lambda/extract.py $DIR/extract/extract.py
cp lambda/insert.py $DIR/insert/insert.py

git clone https://github.com/jkehler/awslambda-psycopg2.git $DIR/insert
mv $DIR/insert/awslambda-psycopg2/psycopg2-3.6 $DIR/insert/psycopg2
rm -rf $DIR/insert/awslambda-psycopg2

pip3 install bs4 -t $DIR/extract

cd deploy/extract
zip -r ../extract.zip *
cd ../..

cd deploy/insert
zip -r ../insert.zip *
cd ../..

rm -rf $DIR/extract
rm -rf $DIR/insert
