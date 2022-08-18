#!/bin/bash

# Script to collect all tweets from:
#	- @FacebooksTop10
#	- @citizenbrowser (Trending on Facebook)
#-------------------------------------------------

today=$(date +"%Y-%m-%d")

# Pull @FacebooksTop10
twarc2 search "from:1285358566300237826" --start-time 2015-01-01 --end-time $today --limit 5000 --archive fb_top10_tweets_${today}.json
echo 'Flattening output file so each line is one tweet...'
twarc2 flatten fb_top10_tweets_${today}.json fb_top10_tweets_flattened_${today}.jsonl

# Pull #citizenbrowser
twarc2 search "from:1451590999088803841" --start-time 2015-01-01 --end-time $today --limit 5000 --archive citizenbrowser_tweets_${today}.json
echo 'Flattening output file so each line is one tweet...'
twarc2 flatten citizenbrowser_tweets_${today}.json citizenbrowser_tweets_flattened_${today}.jsonl
echo '--- script complete ---'
