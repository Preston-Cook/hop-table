import sys
from subprocess import Popen, PIPE
import requests
import re
from tabulate import tabulate

# Initialize pattern for regex
pattern = r'((?:(?:2[0-5]{2}|1\d{2}|[1-9]\d|\d)(?:\.|\s|$)){4})'

# Initialize param for API call
params = {"token": ""} # <-- insert your token here

# Initialize API endpoint
endpoint = "https://ipinfo.io/"

# Usage validation
if len(sys.argv) != 2:
    print("Usage: hop_visialization.py \"url/ip\"")
    sys.exit(1)

# Run Unix cmd and read from stdin
p = Popen(["traceroute", "-n", sys.argv[-1]], stdout=PIPE)

hop_lst = []

while True:
    line = p.stdout.readline()
    hop_lst.append(line.decode('utf-8').strip())
    if not line:
        break

# Initialize table headers and record array
headers = [
    "HOP NUM",
    "IP",
    "ORG",
    "CITY",
    "REGION",
    "COUNTRY",
    "ZIP",
    "LAT, LNG"
]

records = []


# Check traceroute output for ip addresses
for count, hop in enumerate(hop_lst, start=1):
    if (match:= re.search(pattern, hop)):
        ip = match.group(1)

        # Attempt API call with ip and token as params
        try:
            req = requests.get(endpoint + ip, params=params)
            req.raise_for_status()
        
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        
        # Turn string into JSON obj
        resp = req.json()
        
        # Append hop data to records array
        records.append([
            count,
            ip,
            resp.get('org'),
            resp.get('city'),
            resp.get("region"),
            resp.get('country'),
            resp.get('postal'),
            resp.get('loc')
        ])

# Created formatted table str
table = tabulate(records, headers, tablefmt="grid")

# Write table to file
with open("hops-visualization.txt", "w") as fh:
    fh.write(table)

# Print table to terminal
print(table) 
