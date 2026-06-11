# Subscraper Commands

## About

Subscraper is used for:
- subdomain enumeration
- passive reconnaissance
- asset discovery
- bug bounty reconnaissance

It gathers subdomains from:
- search engines
- public APIs
- certificate transparency logs
- OSINT sources

Useful for:
- recon
- attack surface mapping
- asset discovery

Repository:
https://github.com/m8r0wn/subscraper

---

# BASIC COMMANDS

## Basic Enumeration

subscraper -d example.com

---

## Save Output

subscraper -d example.com -o subdomains.txt

---

## Silent Mode

subscraper -d example.com --silent

---

# INPUT OPTIONS

## Multiple Domains

subscraper -l domains.txt

---

## Scan Subdomains

subscraper -d test.example.com

---

# OUTPUT OPTIONS

## JSON Output

subscraper -d example.com --json

---

## TXT Output

subscraper -d example.com -o output.txt

---

## Verbose Output

subscraper -d example.com -v

---

# SOURCE OPTIONS

## Use All Sources

subscraper -d example.com --all

---

## Specify Sources

subscraper -d example.com --sources crtsh,virustotal

---

## Exclude Sources

subscraper -d example.com --exclude censys

---

# THREADING OPTIONS

## Set Threads

subscraper -d example.com --threads 50

---

## Timeout Configuration

subscraper -d example.com --timeout 30

---

# FILTERING OPTIONS

## Remove Wildcards

subscraper -d example.com --no-wildcards

---

## Deduplicate Results

subscraper -d example.com | sort -u

---

# RESOLVER OPTIONS

## Custom Resolvers

subscraper -d example.com --resolver resolvers.txt

---

# API CONFIGURATION

## Use API Keys

subscraper -d example.com --config config.yaml

---

# PIPELINE EXAMPLES

## Subscraper + HTTPX

subscraper -d example.com \
| httpx -silent

---

## Save Alive Hosts

subscraper -d example.com \
| httpx -silent \
> alive.txt

---

## Full Recon Pipeline

subscraper -d example.com \
| httpx -silent \
| tee alive.txt

katana -list alive.txt -silent

---

# AUTOMATION EXAMPLES

## Passive Recon

subscraper -d example.com \
-o passive_subs.txt

---

## Asset Discovery

subscraper -d example.com \
| sort -u \
> assets.txt

---

## Combine With Amass

subscraper -d example.com > subs1.txt

amass enum -passive -d example.com -o subs2.txt

cat subs1.txt subs2.txt | sort -u

---

# ADVANCED COMMANDS

## Recursive Enumeration

subscraper -d example.com --recursive

---

## Aggressive Enumeration

subscraper -d example.com --aggressive

---

## DNS Validation

subscraper -d example.com --validate

---

## Include IP Addresses

subscraper -d example.com --ip

---

# BUG BOUNTY WORKFLOWS

## Asset Collection

subscraper -d example.com \
| httpx -silent \
> alive.txt

---

## Subdomain Takeover Recon

subscraper -d example.com \
| httpx -silent -title

---

## API Subdomain Discovery

subscraper -d example.com \
| grep api

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -d | target domain |
| -l | domain list |
| -o | output file |
| --json | JSON output |
| --all | all sources |
| --sources | specific sources |
| --exclude | exclude sources |
| --threads | concurrency |
| --timeout | timeout |
| --resolver | custom resolvers |
| --silent | silent mode |
| -v | verbose |

---

# BEST PRACTICES

## Combine Multiple Tools

Use:
- subfinder
- amass
- findomain
- subscraper

for better coverage.

---

## Validate Results

Always verify with:
httpx

---

## Deduplicate Outputs

Use:
sort -u

---

## Use Passive First

Avoid detection during reconnaissance.

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent > subs1.txt

subscraper -d example.com > subs2.txt

amass enum -passive -d example.com -o subs3.txt

cat subs1.txt subs2.txt subs3.txt \
| sort -u \
> final_subdomains.txt

httpx -l final_subdomains.txt -silent \
> alive.txt

---

# TROUBLESHOOTING

## No Results

Try:
- enabling all sources
- checking internet connectivity
- API configuration

---

## Slow Enumeration

Reduce:
- threads
- timeout

---

## Tool Not Found

Ensure:
- Python installed
- PATH configured

---

# LIMITATIONS

Subscraper:
- relies on passive sources
- may miss live-only subdomains
- API limits may apply

Use with:
- amass
- subfinder
- findomain

for maximum coverage.

---

# HELP MENU

subscraper --help