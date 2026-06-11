# Feroxbuster Commands

## About

Feroxbuster is used for:
- directory brute forcing
- hidden file discovery
- recursive content enumeration
- endpoint discovery

It is known for:
- speed
- recursive scanning
- smart filtering
- Rust-based performance

Useful for:
- bug bounty
- VAPT
- API discovery
- admin panel discovery

Repository:
https://github.com/epi052/feroxbuster

---

# BASIC COMMANDS

## Basic Scan

feroxbuster -u https://example.com

---

## Save Output

feroxbuster -u https://example.com -o output.txt

---

## Scan Multiple Targets

feroxbuster --stdin

Example:

cat targets.txt | feroxbuster --stdin

---

# WORDLIST OPTIONS

## Custom Wordlist

feroxbuster -u https://example.com \
-w wordlist.txt

---

## Large Wordlist

feroxbuster -u https://example.com \
-w /usr/share/seclists/Discovery/Web-Content/common.txt

---

## Multiple Wordlists

feroxbuster -u https://example.com \
-w admin.txt

---

# EXTENSION OPTIONS

## Scan PHP Files

feroxbuster -u https://example.com -x php

---

## Multiple Extensions

feroxbuster -u https://example.com \
-x php,txt,html,js

---

## Backup Files

feroxbuster -u https://example.com \
-x zip,bak,old,tar,gz

---

# THREADING OPTIONS

## Set Threads

feroxbuster -u https://example.com -t 50

---

## High-Speed Scan

feroxbuster -u https://example.com \
-t 100

---

# RECURSIVE SCANNING

## Recursive Scan

feroxbuster -u https://example.com -r

---

## Limit Recursion Depth

feroxbuster -u https://example.com \
-d 3

---

## Force Recursion

feroxbuster -u https://example.com \
-r --force-recursion

---

# STATUS CODE FILTERING

## Filter Status Codes

feroxbuster -u https://example.com \
-s 200,301,302

---

## Exclude Status Codes

feroxbuster -u https://example.com \
-C 404

---

## Exclude Multiple Codes

feroxbuster -u https://example.com \
-C 403,404,500

---

# PROXY OPTIONS

## Burp Proxy

feroxbuster -u https://example.com \
-p http://127.0.0.1:8080

---

## SOCKS5 Proxy

feroxbuster -u https://example.com \
-p socks5://127.0.0.1:9050

---

# USER AGENT OPTIONS

## Random User-Agent

feroxbuster -u https://example.com \
-random-agent

---

## Custom User-Agent

feroxbuster -u https://example.com \
-H "User-Agent: Mozilla/5.0"

---

# AUTHENTICATION

## Basic Authentication

feroxbuster -u https://example.com \
-U admin -P password

---

## Add Cookies

feroxbuster -u https://example.com \
-H "Cookie: session=abcd"

---

## Add Authorization Header

feroxbuster -u https://example.com \
-H "Authorization: Bearer TOKEN"

---

# OUTPUT OPTIONS

## JSON Output

feroxbuster -u https://example.com \
--json

---

## Silent Mode

feroxbuster -u https://example.com \
-q

---

## Verbose Mode

feroxbuster -u https://example.com \
-v

---

# FILE DISCOVERY

## Find Backup Files

feroxbuster -u https://example.com \
-x bak,zip,old

---

## Find Config Files

feroxbuster -u https://example.com \
-x env,config,ini

---

## Find Database Dumps

feroxbuster -u https://example.com \
-x sql,db

---

# FILTERING OPTIONS

## Filter By Size

feroxbuster -u https://example.com \
-S 1234

---

## Filter By Word Count

feroxbuster -u https://example.com \
-W 20

---

## Filter Redirects

feroxbuster -u https://example.com \
--redirects

---

# API ENUMERATION

## API Discovery

feroxbuster -u https://example.com/api

---

## JSON API Discovery

feroxbuster -u https://example.com/api \
-x json

---

## Swagger Discovery

feroxbuster -u https://example.com \
-w swagger.txt

---

# PIPELINE EXAMPLES

## HTTPX + Feroxbuster

httpx -l alive.txt -silent \
| feroxbuster --stdin

---

## Katana + Feroxbuster

katana -u https://example.com -silent \
| feroxbuster --stdin

---

## Subdomain Pipeline

subfinder -d example.com -silent \
| httpx -silent \
| feroxbuster --stdin

---

# AUTOMATION WORKFLOWS

## Admin Panel Discovery

feroxbuster -u https://example.com \
-w admin.txt

---

## Hidden Upload Endpoint Discovery

feroxbuster -u https://example.com \
| grep upload

---

## Sensitive File Hunting

feroxbuster -u https://example.com \
-x env,git,bak,sql

---

# BUG BOUNTY WORKFLOWS

## Backup File Discovery

feroxbuster -u https://example.com \
-x zip,bak,old

---

## API Endpoint Enumeration

feroxbuster -u https://example.com/api \
-r

---

## Admin Enumeration

feroxbuster -u https://example.com \
-w admin-panels.txt

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent > subs.txt

httpx -l subs.txt -silent > alive.txt

katana -list alive.txt -silent > urls.txt

feroxbuster --stdin \
-w /usr/share/seclists/Discovery/Web-Content/common.txt \
< alive.txt

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -u | target URL |
| -w | wordlist |
| -x | extensions |
| -t | threads |
| -r | recursive |
| -d | recursion depth |
| -s | include status codes |
| -C | exclude status codes |
| -H | headers |
| -p | proxy |
| -q | quiet |
| -v | verbose |
| --json | JSON output |

---

# BEST PRACTICES

## Use HTTPX First

Validate alive hosts before scanning.

---

## Avoid Very High Threads

High concurrency can:
- trigger WAFs
- cause bans
- overload targets

---

## Combine With Katana

Katana:
- discovers URLs

Feroxbuster:
- brute-forces hidden content

---

## Filter Noise

Exclude:
- 404 pages
- wildcard responses
- redirects

---

# TROUBLESHOOTING

## Too Many Requests

Reduce:
- threads
- recursion
- request rate

---

## False Positives

Use:
- status filtering
- word filtering
- size filtering

---

## Tool Not Found

Ensure:
- feroxbuster installed
- executable in PATH

---

# LIMITATIONS

Feroxbuster:
- aggressive active scanner
- noisy
- may trigger WAFs

Use only during:
- authorized VAPT
- permitted bug bounty testing

---

# HELP MENU

feroxbuster --help