# Amass Commands

## About

Amass is used for:
- subdomain enumeration
- attack surface mapping
- ASN discovery
- DNS intelligence
- passive + active recon

Repository:
https://github.com/owasp-amass/amass

---

# BASIC COMMANDS

## Basic Passive Enumeration

amass enum -passive -d example.com

---

## Active Enumeration

amass enum -active -d example.com

---

## Save Output

amass enum -passive -d example.com -o amass.txt

---

## Verbose Mode

amass enum -passive -d example.com -v

---

## Silent Mode

amass enum -passive -d example.com -silent

---

# ENUMERATION MODES

## Passive Enumeration

amass enum -passive -d example.com

Uses:
- crt.sh
- VirusTotal
- Shodan
- Censys
- APIs

No direct interaction with target.

---

## Active Enumeration

amass enum -active -d example.com

Performs:
- DNS resolution
- brute forcing
- zone transfers
- certificate checks

---

## Brute Force Enumeration

amass enum -brute -d example.com

---

## Recursive Enumeration

amass enum -brute -min-for-recursive 2 -d example.com

---

# INPUT OPTIONS

## Multiple Domains

amass enum -df domains.txt

---

## Include Subdomains

amass enum -d test.example.com

---

# OUTPUT OPTIONS

## JSON Output

amass enum -json output.json -d example.com

---

## TXT Output

amass enum -o subdomains.txt -d example.com

---

## Log File

amass enum -log amass.log -d example.com

---

# DATA SOURCE OPTIONS

## Show Sources

amass enum -list

---

## Use Specific Sources

amass enum -src -d example.com

---

## Exclude Sources

amass enum -exclude crtsh,censys -d example.com

---

# DNS OPTIONS

## Custom Resolvers

amass enum -rf resolvers.txt -d example.com

---

## IPv4 Only

amass enum -ipv4 -d example.com

---

## IPv6 Only

amass enum -ipv6 -d example.com

---

# BRUTE FORCE OPTIONS

## Wordlist Brute Force

amass enum -brute -w wordlist.txt -d example.com

---

## Alteration Mode

amass enum -aw alterations.txt -d example.com

---

# ASN ENUMERATION

## Enumerate ASN

amass intel -asn 13335

---

## Organization Enumeration

amass intel -org "Google LLC"

---

## CIDR Enumeration

amass intel -cidr 8.8.8.0/24

---

# REVERSE WHOIS

## Reverse Whois Search

amass intel -whois -d example.com

---

# VISUALIZATION

## Generate Graph Database

amass viz -d3 graph.html

---

## Neo4j Integration

amass db -dir amass_db

---

# DATABASE COMMANDS

## Create Database

amass db -dir amass_db

---

## Import Enumeration

amass db -import enumeration.json

---

## Export Enumeration

amass db -export output.json

---

# ADVANCED COMMANDS

## High Recursion

amass enum -brute -min-for-recursive 1 -d example.com

---

## Maximum DNS Queries

amass enum -max-dns-queries 200 -d example.com

---

## Timeout Configuration

amass enum -timeout 60 -d example.com

---

## Disable Alterations

amass enum -noalts -d example.com

---

# CLOUD ENUMERATION

## AWS Enumeration

amass intel -org Amazon

---

## Azure Enumeration

amass intel -org Microsoft

---

# API CONFIGURATION

## Use API Config File

amass enum -config config.ini -d example.com

---

# EXAMPLE AUTOMATION COMMANDS

## Recon Pipeline Usage

amass enum -passive -d example.com -o amass.txt

---

## Aggressive Enumeration

amass enum -active -brute -min-for-recursive 2 -d example.com -o aggressive.txt

---

## Combined With HTTPX

amass enum -passive -d example.com -o subs.txt

cat subs.txt | httpx

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -passive | passive mode |
| -active | active mode |
| -brute | brute force |
| -src | show source |
| -ip | show IPs |
| -ipv4 | IPv4 only |
| -ipv6 | IPv6 only |
| -o | output file |
| -json | JSON output |
| -v | verbose |
| -silent | silent output |
| -timeout | timeout |
| -w | wordlist |
| -rf | resolver file |

---

# BEST PRACTICES

## Passive First

Use passive mode initially to avoid detection.

---

## Use Custom Resolvers

Avoid public resolver rate limits.

---

## Combine With HTTPX

Validate alive hosts after enumeration.

---

## Store JSON Outputs

Useful for automation pipelines.

---

# PIPELINE EXAMPLE

amass enum -passive -d example.com -o subs.txt

httpx -l subs.txt -silent -o alive.txt

katana -list alive.txt -silent -o urls.txt

gf xss urls.txt

dalfox file xss.txt

---

# TROUBLESHOOTING

## Tool Not Found

Ensure:
- Go installed
- GOPATH configured
- amass added to PATH

---

## Resolver Errors

Use:
amass enum -rf resolvers.txt

---

## Slow Enumeration

Reduce:
- brute force
- recursive depth
- DNS queries

---

# HELP MENU

amass -h

amass enum -h

amass intel -h

amass viz -h