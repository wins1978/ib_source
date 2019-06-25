#!/bin/sh

cnt1=`ps -ef | grep "ib_data_collection/run.sh" | grep -v "grep" | grep -v "crontab.log" | wc -l `
if [ $cnt1 -eq 1 ]; then
    ids=`ps -ef | grep "ib_data_collection/run.sh" | grep -v "grep" | grep -v "crontab.log"| awk '{print $2}'` 
    kill -9 $ids
fi

cnt=`ps -ef | grep "main.py by_day" | grep -v "grep" | grep -v "crontab.log" | wc -l`
echo $cnt
if [ $cnt -ge 1 ]; then
    exit
else
    echo "run..." >> ./temp.log
    /usr/bin/python /data/ib_data_collection/main.py by_day
fi

