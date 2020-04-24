#!/bin/bash

count=0
while (true)
do
 echo "Start"
 python3 fresh_news.py
 echo "Sleeping 1 minute"
 echo $count
 count=$[ $count + 1 ]
 sleep 60
done
