#!/usr/bin/env bash

# https://www.researchgate.net/post/Does-anyone-know-of-an-online-repository-where-its-possible-to-look-up-updated-half-life-and-decay-constant-values
# to http://www.nucleide.org/DDEP_WG/DDEPdata.htm
# 221 nuclides
wget -c -N --accept-regex='.*lara.txt' -r http://www.nucleide.org/DDEP_WG/DDEPdata.htm