# Dirsearch Commands

## About

Dirsearch is used for:
- directory brute forcing
- file discovery
- hidden endpoint enumeration
- web content discovery

Useful for:
- admin panel discovery
- backup file discovery
- API endpoint discovery
- bug bounty reconnaissance

Repository:
https://github.com/maurosoria/dirsearch

---

# BASIC COMMANDS

## Basic Scan

dirsearch -u https://example.com

---

## Save Output

dirsearch -u https://example.com -o output.txt

---

## Scan Multiple Targets

dirsearch -l targets.txt

---

# WORDLIST OPTIONS

## Custom Wordlist

dirsearch -u https://example.com \
-w wordlist.txt

---

## Multiple Wordlists

dirsearch -u https://example.com \
-w admin.txt,api.txt

---

## Large Wordlist

dirsearch -u https://example.com \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

---

# EXTENSION OPTIONS

## PHP Files

dirsearch -u https://example.com -e php

---

## Multiple Extensions

dirsearch -u https://example.com \
-e php,asp,aspx,jsp,js,txt

---

## Backup Files

dirsearch -u https://example.com \
-e zip,bak,old,tar,gz

---

# THREADING OPTIONS

## Set Threads

dirsearch -u https://example.com -t 50

---

## High-Speed Scan

dirsearch -u https://example.com \
-t 100

---

# STATUS CODE FILTERING

## Exclude 403

dirsearch -u https://example.com \
-x 403

---

## Include Only 200

dirsearch -u https://example.com \
-i 200

---

## Exclude Multiple Codes

dirsearch -u https://example.com \
-x 403,404,500

---

# RECURSIVE SCANNING

## Recursive Enumeration

dirsearch -u https://example.com -r

---

## Deep Recursive Scan

dirsearch -u https://example.com \
-r --deep-recursive

---

# PROXY OPTIONS

## Burp Proxy

dirsearch -u https://example.com \
--proxy=http://127.0.0.1:8080

---

## SOCKS5 Proxy

dirsearch -u https://example.com \
--proxy=socks5://127.0.0.1:9050

---

# AUTHENTICATION

## Basic Authentication

dirsearch -u https://example.com \
--auth admin:password

---

## Add Cookies

dirsearch -u https://example.com \
-H "Cookie: session=abcd"

---

## Add Authorization Header

dirsearch -u https://example.com \
-H "Authorization: Bearer TOKEN"

---

# USER AGENT

## Random User-Agent

dirsearch -u https://example.com \
--random-agent

---

## Custom User-Agent

dirsearch -u https://example.com \
-H "User-Agent: Mozilla/5.0"

---

# OUTPUT OPTIONS

## JSON Output

dirsearch -u https://example.com \
--format json

---

## HTML Report

dirsearch -u https://example.com \
--format html

---

## Plain Text Output

dirsearch -u https://example.com \
--plain-text-report report.txt

---

# FILTERING OPTIONS

## Filter By Size

dirsearch -u https://example.com \
--exclude-sizes=1234B

---

## Filter By Text

dirsearch -u https://example.com \
--exclude-text="Not Found"

---

## Filter Redirects

dirsearch -u https://example.com \
--follow-redirects

---

# FILE DISCOVERY

## Discover Backup Files

dirsearch -u https://example.com \
-e bak,zip,old

---

## Find Config Files

dirsearch -u https://example.com \
-e env,config,ini

---

## Find Database Dumps

dirsearch -u https://example.com \
-e sql,db

---

# API ENUMERATION

## API Discovery

dirsearch -u https://example.com/api \
-e json

---

## Swagger Discovery

dirsearch -u https://example.com \
-w swagger.txt

---

# PIPELINE EXAMPLES

## HTTPX + Dirsearch

httpx -l alive.txt -silent \
| dirsearch --stdin

---

## Katana + Dirsearch

katana -u https://example.com -silent \
| dirsearch --stdin

---

## Subdomain Recon Pipeline

subfinder -d example.com -silent \
| httpx -silent \
| dirsearch --stdin

---

# AUTOMATION WORKFLOWS

## Admin Panel Discovery

dirsearch -u https://example.com \
-w admin.txt

---

## Backup File Hunting

dirsearch -u https://example.com \
-e zip,bak,old

---

## Hidden API Discovery

dirsearch -u https://example.com/api \
-r

---

# BUG BOUNTY WORKFLOWS

## Sensitive File Discovery

dirsearch -u https://example.com \
-e env,git,sql,bak

---

## Admin Enumeration

dirsearch -u https://example.com \
-w admin-panels.txt

---

## Upload Endpoint Discovery

dirsearch -u https://example.com \
| grep upload

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent > subs.txt

httpx -l subs.txt -silent > alive.txt

katana -list alive.txt -silent > urls.txt

dirsearch -l alive.txt \
-e php,js,txt,zip \
-r

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -u | target URL |
| -l | target list |
| -w | wordlist |
| -e | extensions |
| -t | threads |
| -r | recursive |
| -x | exclude status codes |
| -i | include status codes |
| -H | custom headers |
| --proxy | use proxy |
| --random-agent | random user agent |
| --format | report format |

---

# BEST PRACTICES

## Use Large Wordlists Carefully

Large lists increase:
- scan time
- detection risk

---

## Use HTTPX First

Verify alive hosts before scanning.

---

## Exclude Noise

Exclude:
- 403
- 404
- static pages

---

## Combine With Katana

Katana discovers endpoints.
Dirsearch brute-forces hidden paths.

---

# TROUBLESHOOTING

## Too Many Requests

Reduce:
- threads
- request rate

---

## False Positives

Use:
--exclude-text

---

## Tool Not Found

Ensure:
- Python installed
- dirsearch installed
- PATH configured

---

# LIMITATIONS

Dirsearch:
- noisy active scanning
- may trigger WAFs
- rate limits possible

Use carefully during:
- VAPT
- bug bounty
- authorized testing

---

# HELP MENU

dirsearch --help