# ParamSpider Commands

## About

ParamSpider is used for:
- parameter discovery
- archived URL analysis
- hidden parameter enumeration
- bug bounty reconnaissance

It extracts parameters from:
- Wayback Machine
- archived endpoints
- historical URLs

Useful for:
- XSS
- SQLi
- SSRF
- IDOR
- Open Redirects

Repository:
https://github.com/devanshbatham/ParamSpider

---

# BASIC COMMANDS

## Basic Scan

paramspider -d example.com

---

## Save Output

paramspider -d example.com -o results.txt

---

## Crawl Subdomains

paramspider -d example.com --subs

---

# OUTPUT OPTIONS

## Output Directory

paramspider -d example.com -o output/

---

## Save Parameters Only

paramspider -d example.com \
| grep "="

---

# FILTERING OPTIONS

## Exclude Extensions

paramspider -d example.com \
--exclude woff,css,js,png,svg,jpg

---

## Custom Exclusions

paramspider -d example.com \
--exclude php,jpg,png

---

# PIPELINE EXAMPLES

## ParamSpider + GF

paramspider -d example.com \
| gf xss

---

## ParamSpider + Dalfox

paramspider -d example.com \
| gf xss \
| dalfox pipe

---

## ParamSpider + SQLMap

paramspider -d example.com \
| gf sqli \
> sqli.txt

sqlmap -m sqli.txt --batch

---

# PARAMETER DISCOVERY

## Find XSS Parameters

paramspider -d example.com \
| gf xss

---

## Find SQLi Parameters

paramspider -d example.com \
| gf sqli

---

## Find SSRF Parameters

paramspider -d example.com \
| gf ssrf

---

## Find LFI Parameters

paramspider -d example.com \
| gf lfi

---

# URL FILTERING

## URLs With Parameters

paramspider -d example.com \
| grep "="

---

## Filter Login Endpoints

paramspider -d example.com \
| grep login

---

## Filter API Endpoints

paramspider -d example.com \
| grep api

---

# AUTOMATION WORKFLOWS

## XSS Recon Workflow

paramspider -d example.com \
| gf xss \
| dalfox pipe

---

## SQLi Recon Workflow

paramspider -d example.com \
| gf sqli \
| sqlmap --batch

---

## SSRF Recon Workflow

paramspider -d example.com \
| gf ssrf

---

# FILE EXTRACTION

## Extract JS URLs

paramspider -d example.com \
| grep ".js"

---

## Extract PHP URLs

paramspider -d example.com \
| grep ".php"

---

## Extract ASPX URLs

paramspider -d example.com \
| grep ".aspx"

---

# ADVANCED COMMANDS

## High Threading

paramspider -d example.com --threads 50

---

## Custom User-Agent

paramspider -d example.com \
--user-agent "Mozilla/5.0"

---

## Use Proxy

paramspider -d example.com \
--proxy http://127.0.0.1:8080

---

# COMBINED RECON PIPELINE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

katana -list alive.txt -silent -o urls.txt

paramspider -d example.com \
| gf xss \
> xss.txt

dalfox file xss.txt

---

# BUG BOUNTY WORKFLOWS

## Open Redirect Hunting

paramspider -d example.com \
| gf redirect

---

## IDOR Hunting

paramspider -d example.com \
| grep -E "id=|user=|account="

---

## Sensitive Parameter Discovery

paramspider -d example.com \
| grep -Ei "token=|key=|secret=|auth="

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -d | target domain |
| --subs | include subdomains |
| -o | output file |
| --exclude | exclude extensions |
| --proxy | use proxy |
| --threads | concurrency |
| --user-agent | custom agent |

---

# BEST PRACTICES

## Combine With GF

GF helps identify:
- XSS
- SQLi
- SSRF
- LFI

---

## Remove Static Files

Exclude:
- CSS
- images
- fonts

Improves result quality.

---

## Use With Dalfox

Excellent XSS workflow.

---

## Store Parameter URLs

Useful for:
- automation
- testing
- bug bounty

---

# TROUBLESHOOTING

## No Output

Try:
- using --subs
- different internet connection
- valid target domain

---

## Slow Execution

Reduce:
--threads

---

## Tool Not Found

Ensure:
- Python installed
- ParamSpider installed
- PATH configured

---

# LIMITATIONS

ParamSpider:
- depends heavily on archived data
- may miss live endpoints
- not a crawler

Use with:
- katana
- gau
- waybackurls

for better coverage.

---

# HELP MENU

paramspider --help