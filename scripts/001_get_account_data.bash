#!/bin/bash

# Script to collect the account data of:
#	- @FacebooksTop10
#	- @citizenbrowser (Trending on Facebook)
#-------------------------------------------------

today=$(date +"%Y-%m-%d")

twarc2 users ../data/account_ids.txt ../data/account_info_${today}.json
