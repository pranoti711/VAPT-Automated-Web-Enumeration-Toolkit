# Findomain Commands

## About

Findomain is used for:
- subdomain enumeration
- passive reconnaissance
- asset discovery
- attack surface mapping

It is known for:
- high speed
- passive enumeration
- API integrations
- large-scale scans

Useful for:
- bug bounty
- VAPT
- OSINT
- recon automation

Repository:
https://github.com/findomain/findomain

---

# BASIC COMMANDS

## Basic Enumeration

findomain -t example.com

---

## Quiet Mode

findomain -t example.com -q

---

## Save Output

findomain -t example.com -o

---

## Save To Custom File

findomain -t example.com -u output.txt

---

# INPUT OPTIONS

## Multiple Domains

findomain -f domains.txt

---

## Enumerate Subdomain

findomain -t test.example.com

---

# OUTPUT OPTIONS

## TXT Output

findomain -t example.com -u subdomains.txt

---

## Quiet Output

findomain -t example.com -q

---

## Monitor Mode

findomain -t example.com --monitor

---

# FILTERING OPTIONS

## Unique Results

findomain -t example.com -q | sort -u

---

## Filter API Subdomains

findomain -t example.com -q | grep api

---

## Filter Dev Subdomains

findomain -t example.com -q | grep dev

---

## Filter Admin Subdomains

findomain -t example.com -q | grep admin

---

# RESOLVER OPTIONS

## Custom Resolver

findomain -t example.com --resolver 1.1.1.1

---

## Multiple Resolvers

findomain -t example.com \
--resolver 1.1.1.1,8.8.8.8

---

# THREADING OPTIONS

## Set Threads

findomain -t example.com --threads 100

---

# API CONFIGURATION

## Use Facebook API

findomain uses:
- Facebook CT
- Spyse
- VirusTotal
- SecurityTrails

Configure APIs in:
~/.config/findomain/

---

# PIPELINE EXAMPLES

## Findomain + HTTPX

findomain -t example.com -q \
| httpx -silent

---

## Save Alive Hosts

findomain -t example.com -q \
| httpx -silent \
> alive.txt

---

## Full Recon Pipeline

findomain -t example.com -q \
> subs.txt

httpx -l subs.txt -silent \
> alive.txt

katana -list alive.txt -silent

---

# AUTOMATION WORKFLOWS

## Passive Recon

findomain -t example.com -q \
> passive_subs.txt

---

## Asset Discovery

findomain -t example.com -q \
| tee assets.txt

---

## Combine With Other Tools

findomain -t example.com -q > subs1.txt

subfinder -d example.com -silent > subs2.txt

amass enum -passive -d example.com -o subs3.txt

cat subs1.txt subs2.txt subs3.txt \
| sort -u

---

# ADVANCED COMMANDS

## Resolve IP Addresses

findomain -t example.com --ip

---

## HTTP Status Checks

findomain -t example.com --http-status

---

## Check HTTPS

findomain -t example.com --https

---

## External Subdomains

findomain -t example.com --external-subdomains

---

# BUG BOUNTY WORKFLOWS

## Discover API Assets

findomain -t example.com -q \
| grep api

---

## Find Dev Environments

findomain -t example.com -q \
| grep -Ei "dev|staging|test"

---

## Subdomain Takeover Recon

findomain -t example.com -q \
| httpx -title -tech-detect

---

# COMBINED RECON EXAMPLE

subfinder -d example.com -silent > subs1.txt

assetfinder --subs-only example.com > subs2.txt

findomain -t example.com -q > subs3.txt

amass enum -passive -d example.com -o subs4.txt

cat subs1.txt subs2.txt subs3.txt subs4.txt \
| sort -u \
> final_subdomains.txt

httpx -l final_subdomains.txt -silent \
> alive.txt

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -t | target domain |
| -f | domain file |
| -q | quiet mode |
| -o | save output |
| -u | custom output file |
| --threads | concurrency |
| --resolver | custom resolver |
| --monitor | monitor subdomains |
| --ip | resolve IPs |
| --http-status | show HTTP status |
| --https | HTTPS checks |

---

# BEST PRACTICES

## Combine Multiple Enumerators

Use:
- findomain
- amass
- subfinder
- assetfinder

for maximum coverage.

---

## Validate Results

Always verify using:
httpx

---

## Deduplicate Results

Use:
sort -u

---

## Passive Recon First

Avoid aggressive active scans initially.

---

# LIMITATIONS

Findomain:
- passive-focused
- API dependent
- may miss brute-force subdomains

Use with:
- amass
- dns brute forcing
- subfinder

for complete recon.

---

# TROUBLESHOOTING

## Empty Results

Try:
- valid target
- configured APIs
- internet connectivity

---

## Duplicate Results

Use:
sort -u

---

## Tool Not Found

Ensure:
- Findomain installed
- executable added to PATH

---

# HELP MENU

findomain --help
