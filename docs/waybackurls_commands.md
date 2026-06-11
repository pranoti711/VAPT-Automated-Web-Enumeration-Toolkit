# Waybackurls Commands

## About

Waybackurls is used for:
- collecting archived URLs
- discovering historical endpoints
- finding old APIs
- parameter harvesting
- hidden page discovery

It fetches URLs from:
- Wayback Machine (archive.org)

Repository:
https://github.com/tomnomnom/waybackurls

---

# BASIC COMMANDS

## Fetch Archived URLs

waybackurls example.com

---

## Save Output

waybackurls example.com > urls.txt

---

## Read Multiple Domains

cat domains.txt | waybackurls

---

# OUTPUT FILTERING

## Remove Duplicates

waybackurls example.com | sort -u

---

## Remove Duplicate Parameters

waybackurls example.com | uro

---

## Save Clean URLs

waybackurls example.com \
| uro \
> clean_urls.txt

---

# PARAMETER DISCOVERY

## URLs With Parameters

waybackurls example.com | grep "="

---

## Extract XSS Candidates

waybackurls example.com | gf xss

---

## Extract SQLi Candidates

waybackurls example.com | gf sqli

---

## Extract SSRF Candidates

waybackurls example.com | gf ssrf

---

## Extract LFI Candidates

waybackurls example.com | gf lfi

---

# FILE FILTERING

## Extract JavaScript Files

waybackurls example.com | grep ".js"

---

## Extract PHP Files

waybackurls example.com | grep ".php"

---

## Extract ASPX Files

waybackurls example.com | grep ".aspx"

---

## Extract API Endpoints

waybackurls example.com | grep api

---

## Extract Backup Files

waybackurls example.com | grep -E ".bak|.zip|.old"

---

# PIPELINE EXAMPLES

## Waybackurls + HTTPX

waybackurls example.com \
| httpx -silent

---

## Waybackurls + Katana

waybackurls example.com \
| katana -silent

---

## Waybackurls + GF

waybackurls example.com \
| gf xss

---

## Waybackurls + Dalfox

waybackurls example.com \
| gf xss \
| dalfox pipe

---

# URL CLEANING

## Sort Unique URLs

waybackurls example.com \
| sort -u

---

## Normalize URLs

waybackurls example.com \
| uro

---

## Remove Static Files

waybackurls example.com \
| grep -Ev ".(png|jpg|jpeg|gif|css|svg|woff|ttf)$"

---

# ADVANCED RECON

## Discover Hidden Admin Panels

waybackurls example.com \
| grep admin

---

## Find Login Pages

waybackurls example.com \
| grep login

---

## Find Upload Endpoints

waybackurls example.com \
| grep upload

---

## Find API Keys

waybackurls example.com \
| grep key

---

## Find Tokens

waybackurls example.com \
| grep token

---

# AUTOMATION WORKFLOWS

## Historical URL Collection

waybackurls example.com \
> historical_urls.txt

---

## XSS Recon Workflow

waybackurls example.com \
| gf xss \
| dalfox pipe

---

## SQLi Recon Workflow

waybackurls example.com \
| gf sqli

---

## JS Recon Workflow

waybackurls example.com \
| grep ".js" \
> js_files.txt

---

# BUG BOUNTY WORKFLOWS

## Sensitive File Discovery

waybackurls example.com \
| grep -Ei ".env|config|backup|dump"

---

## Admin Discovery

waybackurls example.com \
| grep admin

---

## Open Redirect Discovery

waybackurls example.com \
| gf redirect

---

# COMBINED RECON EXAMPLE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

waybackurls example.com \
| uro \
| tee urls.txt

gf xss urls.txt

dalfox file urls.txt

---

# BEST PRACTICES

## Always Deduplicate URLs

Use:
sort -u

or:
uro

---

## Filter Static Files

Exclude:
- images
- fonts
- CSS

Improves recon quality.

---

## Combine With GF

Useful for:
- XSS
- SQLi
- SSRF
- LFI

---

## Store Historical URLs

Historical URLs often expose:
- old APIs
- hidden admin panels
- deleted endpoints

---

# COMMON PIPELINES

## XSS Pipeline

waybackurls example.com \
| gf xss \
| dalfox pipe

---

## SQLi Pipeline

waybackurls example.com \
| gf sqli

---

## SSRF Pipeline

waybackurls example.com \
| gf ssrf

---

## JS Discovery Pipeline

waybackurls example.com \
| grep ".js"

---

# TROUBLESHOOTING

## Empty Output

Try:
- checking internet connection
- target validity

---

## Duplicate URLs

Use:
sort -u
or:
uro

---

## Tool Not Found

Ensure:
- Go installed
- PATH configured

---

# LIMITATIONS

Waybackurls:
- only uses archive.org
- may miss live endpoints
- does not crawl actively

Use with:
- katana
- gau
- hakrawler

for better coverage.

---

# HELP MENU

waybackurls --help