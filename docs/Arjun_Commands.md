# Arjun Commands

## About

Arjun is used for:
- hidden parameter discovery
- GET/POST parameter fuzzing
- endpoint analysis
- API parameter enumeration

Useful for:
- XSS
- SQLi
- SSRF
- IDOR
- access control testing

Repository:
https://github.com/s0md3v/Arjun

---

# BASIC COMMANDS

## Scan Single URL

arjun -u https://example.com

---

## Save Output

arjun -u https://example.com -oT output.txt

---

## JSON Output

arjun -u https://example.com -oJ output.json

---

## HTTP Method Selection

arjun -u https://example.com -m GET

---

## POST Request Testing

arjun -u https://example.com/login -m POST

---

# INPUT OPTIONS

## Scan Multiple URLs

arjun -i targets.txt

---

## Import From File

arjun -i urls.txt -oT results.txt

---

# PARAMETER DISCOVERY

## GET Parameter Discovery

arjun -u https://example.com/page.php

---

## POST Parameter Discovery

arjun -u https://example.com/api -m POST

---

## JSON Body Testing

arjun -u https://example.com/api \
-m POST \
--json

---

# CUSTOM HEADERS

## Add Authorization Header

arjun -u https://example.com \
-H "Authorization: Bearer token"

---

## Custom User-Agent

arjun -u https://example.com \
-H "User-Agent: Mozilla"

---

## Add Cookies

arjun -u https://example.com \
-H "Cookie: session=abcd"

---

# THREADING OPTIONS

## Set Threads

arjun -u https://example.com -t 50

---

## Request Delay

arjun -u https://example.com -d 2

---

## Timeout

arjun -u https://example.com --timeout 20

---

# WORDLIST OPTIONS

## Custom Wordlist

arjun -u https://example.com \
-w wordlist.txt

---

## Large Wordlist

arjun -u https://example.com \
--stable

---

# RATE LIMITING

## Slow Scan

arjun -u https://example.com \
--rate 5

---

# PROXY OPTIONS

## Burp Proxy

arjun -u https://example.com \
--proxy http://127.0.0.1:8080

---

## SOCKS5 Proxy

arjun -u https://example.com \
--proxy socks5://127.0.0.1:9050

---

# OUTPUT OPTIONS

## Text Output

arjun -u https://example.com -oT output.txt

---

## JSON Output

arjun -u https://example.com -oJ output.json

---

## Save Discovered Parameters

arjun -u https://example.com \
-oT params.txt

---

# PIPELINE EXAMPLES

## Arjun + GF

arjun -u https://example.com \
-oT params.txt

cat params.txt | gf xss

---

## Arjun + Dalfox

arjun -u https://example.com \
-oT params.txt

cat params.txt | dalfox pipe

---

## Arjun + SQLMap

arjun -u https://example.com \
-oT params.txt

sqlmap -m params.txt --batch

---

# API TESTING

## API Parameter Discovery

arjun -u https://api.example.com/users

---

## JSON API Testing

arjun -u https://api.example.com/login \
-m POST \
--json

---

# BUG BOUNTY WORKFLOWS

## XSS Recon

arjun -u https://example.com \
-oT params.txt

cat params.txt | gf xss

---

## SQLi Recon

arjun -u https://example.com \
-oT params.txt

cat params.txt | gf sqli

---

## SSRF Recon

arjun -u https://example.com \
-oT params.txt

cat params.txt | gf ssrf

---

# ADVANCED COMMANDS

## Passive Mode

arjun -u https://example.com --passive

---

## Disable Redirects

arjun -u https://example.com \
--disable-redirects

---

## Include Stable Parameters

arjun -u https://example.com \
--stable

---

## Verbose Mode

arjun -u https://example.com -v

---

# AUTOMATION EXAMPLES

## Discover Hidden Parameters

arjun -u https://example.com \
-oT hidden_params.txt

---

## Bulk URL Scanning

arjun -i urls.txt \
-oT all_params.txt

---

## API Recon Workflow

gau example.com \
| grep api \
> api.txt

arjun -i api.txt

---

# COMPLETE RECON PIPELINE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

katana -list alive.txt -silent -o urls.txt

grep "=" urls.txt > params.txt

arjun -i params.txt -oT discovered.txt

gf xss discovered.txt

dalfox file discovered.txt

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -u | target URL |
| -i | input file |
| -m | request method |
| -oT | text output |
| -oJ | JSON output |
| -t | threads |
| -d | delay |
| -w | wordlist |
| -H | custom header |
| --proxy | proxy |
| --json | JSON requests |
| --stable | stable mode |
| -v | verbose |

---

# BEST PRACTICES

## Use With Katana

Katana discovers endpoints.
Arjun discovers hidden parameters.

---

## Use With Dalfox

Excellent for XSS workflows.

---

## Use Burp Proxy

Useful for:
- debugging
- request inspection
- authentication testing

---

## Store JSON Outputs

Helpful for:
- automation
- pipelines
- reporting

---

# TROUBLESHOOTING

## No Parameters Found

Try:
- authenticated endpoints
- POST requests
- API endpoints

---

## Slow Scanning

Reduce:
- threads
- rate
- timeout

---

## Tool Not Found

Ensure:
- Python installed
- Arjun installed
- PATH configured

---

# LIMITATIONS

Arjun:
- focuses on parameter discovery
- does not crawl deeply
- works best with known endpoints

Use with:
- katana
- gau
- waybackurls

for best results.

---

# HELP MENU

arjun --help