### How to do complicated search in Wikipedia.

Download [Wikipedia dump](https://meta.wikimedia.org/wiki/Data_dump_torrents) with torrent.

Unpack .bz2 file with `bzip2 -d *` - you will get xml file ~75 GB.

Get all articke content from dump with words "developing countr,third world" into file `processed` in half an hour.

    python3 search_wiki.py enwiki-20201101-pages-articles-multistream.xml processed "developing countr,third world"

Restrict search to articles with words `technology,tool,device`

    python3 search_wiki.py  processed processed2 "technology,tool,device"

To search for articles without  word - add `not` at the end.

    python3 search_wiki.py  processed processed2 people not

To extract article titles from file:

    cat processed | grep "^    <title>" | sed 's/    <title>//g' | sed 's/<\/title>//g' | sort > titles