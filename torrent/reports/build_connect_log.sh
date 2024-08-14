#!/usr/bin/env bash
find .. -name "*.log" -exec cat {} \; |
{
	grep -a "CONNECT" | sed -r 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ - - //g' | sort | sed -r 's/\[(.+)\] "(.+)" (.+) (.+) (.+)/\1\t\2\t\3\t\4\t\5/g'
} > connect_log

cat connect_log |
{
	grep "forum.kerbalspaceprogram.com" | cut -d $'\t' -f 1,5 | sed -r 's/(.+) (..:..):..\t(.+)/\1\t\2\t\3/g'
} > connect_log.time-per-connect.csv

cat connect_log.time-per-connect.csv |
{
	cut -d $'\t' -f 1,2 | uniq -c | awk '{ print($2"\t"$3"\t"$1); }'
} > connect_log.hits-per-minute.csv

