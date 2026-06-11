# HTTPX Commands

## About

HTTPX is used for:
- alive host detection
- HTTP probing
- status code checking
- title grabbing
- tech detection
- screenshotting
- port scanning

Repository:
https://github.com/projectdiscovery/httpx

---

# BASIC COMMANDS

## Check Single Host

httpx -u https://example.com

---

## Check Multiple Hosts

httpx -l hosts.txt

---

## Silent Mode

httpx -l hosts.txt -silent

---

## Save Output

httpx -l hosts.txt -o output.txt

---

## JSON Output

httpx -l hosts.txt -json

---

## CSV Output

httpx -l hosts.txt -csv

---

# STATUS CODE OPTIONS

## Show Status Codes

httpx -l hosts.txt -sc

---

## Filter Status Codes

httpx -l hosts.txt -mc 200,302

---

## Exclude Status Codes

httpx -l hosts.txt -fc 404,500

---

# TITLE OPTIONS

## Fetch Page Titles

httpx -l hosts.txt -title

---

# TECH DETECTION

## Detect Technologies

httpx -l hosts.txt -td

---

## Detect CDN/WAF

httpx -l hosts.txt -cdn

---

# RESPONSE OPTIONS

## Show Content Length

httpx -l hosts.txt -cl

---

## Show Response Time

httpx -l hosts.txt -rt

---

## Show Web Server

httpx -l hosts.txt -server

---

## Show IP Address

httpx -l hosts.txt -ip

---

# PORT OPTIONS

## Scan Specific Ports

httpx -l hosts.txt -ports 80,443,8080

---

## Scan Top Ports

httpx -l hosts.txt -top-ports 100

---

# HTTPS OPTIONS

## Prefer HTTPS

httpx -l hosts.txt -https

---

## Prefer HTTP

httpx -l hosts.txt -no-https

---

## Follow Redirects

httpx -l hosts.txt -follow-redirects

---

## Show Redirect Location

httpx -l hosts.txt -location

---

# SCREENSHOT OPTIONS

## Take Screenshots

httpx -l hosts.txt -ss

---

## Save Screenshot Directory

httpx -l hosts.txt -ss -srd screenshots/

---

# PROBE OPTIONS

## Probe Only Alive Hosts

httpx -l hosts.txt -probe

---

## Probe With Threads

httpx -l hosts.txt -threads 100

---

## Timeout Configuration

httpx -l hosts.txt -timeout 10

---

## Rate Limit

httpx -l hosts.txt -rl 200

---

# FILTERING OPTIONS

## Match Title

httpx -l hosts.txt -match-string admin

---

## Filter By Title

httpx -l hosts.txt -filter-string error

---

## Match Regex

httpx -l hosts.txt -mr "login"

---

## Filter Regex

httpx -l hosts.txt -fr "404"

---

# CUSTOM HEADERS

## Add Header

httpx -l hosts.txt -H "Authorization: Bearer token"

---

## Custom User-Agent

httpx -l hosts.txt -H "User-Agent: Mozilla"

---

# VHOST OPTIONS

## Virtual Host Detection

httpx -l hosts.txt -vhost

---

# TLS OPTIONS

## TLS Probe

httpx -l hosts.txt -tls-probe

---

## Show TLS Info

httpx -l hosts.txt -tls-grab

---

# PIPELINE USAGE

## Subdomain Alive Check

subfinder -d example.com | httpx -silent

---

## Save Alive Hosts

subfinder -d example.com | httpx -silent -o alive.txt

---

## Full Recon Example

subfinder -d example.com -silent \
| httpx -title -tech-detect -status-code

---

# AUTOMATION COMMANDS

## Alive Hosts Only

httpx -l subdomains.txt -silent -o alive.txt

---

## Screenshot Automation

httpx -l alive.txt -ss -srd screenshots/

---

## Tech Detection Automation

httpx -l alive.txt -td -json -o tech.json

---

# ADVANCED OPTIONS

## HTTP2 Detection

httpx -l hosts.txt -http2

---

## Pipeline Support

httpx -l hosts.txt -pipeline

---

## CSP Probe

httpx -l hosts.txt -csp-probe

---

## Favicon Hash

httpx -l hosts.txt -favicon

---

## Extract Response Body

httpx -l hosts.txt -body-preview

---

## Extract Headers

httpx -l hosts.txt -include-response-header

---

# OUTPUT FORMATS

## Store Full Response

httpx -l hosts.txt -store-response

---

## Store Response Directory

httpx -l hosts.txt -store-response-dir responses/

---

## JSON Lines Output

httpx -l hosts.txt -json -o results.json

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -silent | silent mode |
| -sc | status code |
| -title | page title |
| -td | technology detect |
| -ip | show IP |
| -cdn | detect CDN |
| -rt | response time |
| -server | server header |
| -ss | screenshot |
| -json | JSON output |
| -csv | CSV output |
| -o | output file |
| -threads | concurrency |
| -timeout | timeout |
| -rl | rate limit |

---

# BEST PRACTICES

## Use Silent Mode In Pipelines

httpx -silent

Prevents noisy outputs.

---

## Save JSON Outputs

Useful for automation frameworks.

---

## Combine With Katana

httpx → katana → gf → dalfox

---

## Use Rate Limiting

Avoid blocking and bans.

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -title -tech-detect -o alive.txt

katana -list alive.txt -silent -o urls.txt

gf xss urls.txt

dalfox file xss.txt

---

# TROUBLESHOOTING

## Tool Not Found

Ensure:
- Go installed
- GOPATH configured
- PATH updated

---

## Permission Issues

Run terminal as administrator.

---

## Slow Scanning

Reduce:
- threads
- rate limit
- timeout

---

# HELP MENU

httpx -h