# GF Commands

## About

GF (Grep Filter) is used for:
- filtering URLs
- finding vulnerability patterns
- bug bounty recon
- identifying attack surfaces

GF works using predefined patterns for:
- XSS
- SQLi
- SSRF
- LFI
- RCE
- redirects
- secrets
- debug pages

Repository:
https://github.com/tomnomnom/gf

---

# BASIC COMMANDS

## Basic Usage

cat urls.txt | gf xss

---

## SQL Injection Patterns

cat urls.txt | gf sqli

---

## SSRF Patterns

cat urls.txt | gf ssrf

---

## LFI Patterns

cat urls.txt | gf lfi

---

## RCE Patterns

cat urls.txt | gf rce

---

## Redirect Patterns

cat urls.txt | gf redirect

---

# COMMON PATTERNS

## XSS

gf xss

Finds:
- q=
- search=
- callback=
- redirect=
- query=

---

## SQLi

gf sqli

Finds:
- id=
- uid=
- cat=
- item=
- page=

---

## SSRF

gf ssrf

Finds:
- url=
- uri=
- path=
- continue=
- domain=

---

## LFI

gf lfi

Finds:
- file=
- path=
- folder=
- include=
- template=

---

## RCE

gf rce

Finds:
- cmd=
- exec=
- command=
- ping=
- query=

---

## Redirect

gf redirect

Finds:
- next=
- redirect=
- return=
- url=
- continue=

---

# INPUT METHODS

## From File

cat urls.txt | gf xss

---

## Direct Pipe

gau example.com | gf xss

---

## Multiple Files

cat *.txt | gf sqli

---

# PIPELINE EXAMPLES

## GAU + GF

gau example.com \
| gf xss

---

## Waybackurls + GF

waybackurls example.com \
| gf sqli

---

## Katana + GF

katana -u https://example.com -silent \
| gf lfi

---

## HTTPX + GF

cat alive.txt \
| gf redirect

---

# GF + DALFOX

## XSS Workflow

gau example.com \
| gf xss \
| dalfox pipe

---

## XSS File Workflow

cat urls.txt \
| gf xss \
> xss.txt

dalfox file xss.txt

---

# GF + SQLMAP

## SQLi Workflow

gau example.com \
| gf sqli \
> sqli.txt

sqlmap -m sqli.txt --batch

---

# URL FILTERING

## Filter URLs With Parameters

cat urls.txt | grep "="

---

## Filter API URLs

cat urls.txt | grep api

---

## Filter Admin URLs

cat urls.txt | grep admin

---

## Filter Login URLs

cat urls.txt | grep login

---

# CUSTOM PATTERNS

## Create Custom Pattern

gf uses:
~/.gf/

Pattern example:

xss.json

{
  "flags": "-iE",
  "patterns": [
    "q=",
    "search=",
    "callback="
  ]
}

---

# USE CUSTOM PATTERN

cat urls.txt | gf xss

---

# PATTERN LOCATION

## Linux/macOS

~/.gf/

---

## Windows

C:\Users\USERNAME\.gf\

---

# INSTALL DEFAULT PATTERNS

## Clone Gf-Patterns

git clone https://github.com/1ndianl33t/Gf-Patterns

---

## Copy Patterns

cp *.json ~/.gf/

---

# ADVANCED COMMANDS

## Ignore Case

cat urls.txt | gf xss -i

---

## Count Matches

cat urls.txt | gf xss | wc -l

---

## Save Matches

cat urls.txt | gf xss > xss.txt

---

## Remove Duplicate Results

cat urls.txt | gf xss | sort -u

---

# BUG BOUNTY WORKFLOWS

## XSS Hunting

gau example.com \
| gf xss \
| dalfox pipe

---

## SQLi Hunting

waybackurls example.com \
| gf sqli \
| sqlmap --batch

---

## SSRF Hunting

gau example.com \
| gf ssrf

---

## LFI Hunting

katana -u https://example.com \
| gf lfi

---

# COMPLETE RECON PIPELINE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

katana -list alive.txt -silent -o urls.txt

gf xss urls.txt

dalfox file urls.txt

---

# AUTOMATION EXAMPLES

## Save XSS Candidates

gau example.com \
| gf xss \
> xss_candidates.txt

---

## Save SQLi Candidates

gau example.com \
| gf sqli \
> sqli_candidates.txt

---

## Save SSRF Candidates

gau example.com \
| gf ssrf \
> ssrf_candidates.txt

---

# COMMON PATTERN NAMES

| Pattern | Purpose |
|---------|----------|
| xss | XSS parameters |
| sqli | SQL injection |
| ssrf | SSRF |
| lfi | Local file inclusion |
| rce | Remote code execution |
| redirect | Open redirect |
| debug_logic | Debug endpoints |
| img-traversal | Image traversal |
| interestingEXT | Interesting files |
| interestingsubs | Interesting subdomains |

---

# BEST PRACTICES

## Use After URL Collection

Best used after:
- gau
- waybackurls
- katana

---

## Combine With Dalfox

GF filters XSS candidates efficiently.

---

## Use Custom Patterns

Custom patterns improve recon quality.

---

## Deduplicate Results

Always use:
sort -u

---

# TROUBLESHOOTING

## No Patterns Found

Ensure:
~/.gf/

contains JSON patterns.

---

## Empty Output

Try:
- more URLs
- better patterns
- broader recon

---

## Tool Not Found

Ensure:
- Go installed
- PATH configured

---

# HELP MENU

gf -h