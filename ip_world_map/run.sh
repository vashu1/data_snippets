# get ip db with wget
# or download it manually from https://ip2location.com (Free/Lite DB)
wget https://download.ip2location.com/lite/IP2LOCATION-LITE-DB1.CSV.ZIP
unzip IP2LOCATION-LITE-DB1.CSV.ZIP
rm README_LITE.TXT
rm LICENSE-CC-BY-SA-4.0.TXT

# generate countries top and "country_cidrs" file for ipv4-heatmap
echo -e "\nrunning python script..."
python3 code.py

echo -e "\ngenerating map file..."
git clone https://github.com/measurement-factory/ipv4-heatmap.git
cd ipv4-heatmap
make
cd ..
echo "" | ./ipv4-heatmap/ipv4-heatmap -a country_cidrs -o ip_world_map.png

