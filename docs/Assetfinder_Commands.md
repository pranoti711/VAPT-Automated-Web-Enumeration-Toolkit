# Assetfinder Commands

## About

Assetfinder is used for:
- subdomain enumeration
- passive reconnaissance
- asset discovery
- attack surface mapping

It gathers subdomains from:
- certificate transparency logs
- APIs
- public OSINT sources

Useful for:
- bug bounty
- recon automation
- external asset discovery

Repository:
https://github.com/tomnomnom/assetfinder

---

# BASIC COMMANDS

## Basic Enumeration

assetfinder example.com

---

## Subdomains Only

assetfinder --subs-only example.com

---

## Save Output

assetfinder --subs-only example.com > subdomains.txt

---

# INPUT OPTIONS

## Scan Multiple Domains

cat domains.txt | assetfinder

---

## Enumerate Specific Subdomain

assetfinder test.example.com

---

# OUTPUT OPTIONS

## Save Results

assetfinder --subs-only example.com \
> output.txt

---

## Remove Duplicates

assetfinder --subs-only example.com \
| sort -u

---

# PIPELINE EXAMPLES

## Assetfinder + HTTPX

assetfinder --subs-only example.com \
| httpx -silent

---

## Save Alive Hosts

assetfinder --subs-only example.com \
| httpx -silent \
> alive.txt

---

## Full Recon Pipeline

assetfinder --subs-only example.com \
| sort -u \
> subs.txt

httpx -l subs.txt -silent \
> alive.txt

katana -list alive.txt -silent

---

# AUTOMATION WORKFLOWS

## Passive Recon

assetfinder --subs-only example.com \
> passive_subdomains.txt

---

## Asset Discovery

assetfinder --subs-only example.com \
| tee assets.txt

---

## Combine With Amass

assetfinder --subs-only example.com > subs1.txt

amass enum -passive -d example.com -o subs2.txt

cat subs1.txt subs2.txt \
| sort -u

---

# FILTERING OPTIONS

## Filter API Subdomains

assetfinder --subs-only example.com \
| grep api

---

## Filter Dev Subdomains

assetfinder --subs-only example.com \
| grep dev

---

## Filter Admin Panels

assetfinder --subs-only example.com \
| grep admin

---

# ADVANCED USAGE

## Enumerate Hidden Assets

assetfinder example.com \
| sort -u

---

## Combine With GF

assetfinder --subs-only example.com \
| gf interestingsubs

---

# BUG BOUNTY WORKFLOWS

## Alive Asset Discovery

assetfinder --subs-only example.com \
| httpx -title -tech-detect

---

## API Enumeration

assetfinder --subs-only example.com \
| grep api

---

## Dev Environment Discovery

assetfinder --subs-only example.com \
| grep -Ei "dev|staging|test"

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
| --subs-only | show only subdomains |

---

# BEST PRACTICES

## Combine Multiple Enumerators

Use:
- assetfinder
- subfinder
- amass
- findomain

for better coverage.

---

## Validate Results

Always verify using:
httpx

---

## Deduplicate Outputs

Use:
sort -u

---

## Passive Recon First

Avoid active probing initially.

---

# LIMITATIONS

Assetfinder:
- passive only
- limited source coverage
- may miss deep subdomains

Use with:
- amass
- subfinder
- findomain

for maximum results.

---

# TROUBLESHOOTING

## Empty Output

Try:
- valid domain
- internet connection
- combine with other tools

---

## Duplicate Results

Use:
sort -u

---

## Tool Not Found

Ensure:
- Go installed
- PATH configured

---

# HELP MENU

assetfinder --help