# GAU Commands

## About

GAU (GetAllURLs) is used for:
- collecting historical URLs
- archived endpoint discovery
- attack surface mapping
- parameter harvesting
- URL enumeration

GAU gathers URLs from:
- Wayback Machine
- Common Crawl
- AlienVault OTX
- URLScan

Repository:
https://github.com/lc/gau

---

# BASIC COMMANDS

## Collect URLs

gau example.com

---

## Save Output

gau example.com > urls.txt

---

## Multiple Domains

gau -providers wayback example.com

---

## Read Domains From File

cat domains.txt | gau

---

# PROVIDER OPTIONS

## Use Specific Providers

gau --providers wayback,commoncrawl example.com

---

## Wayback Only

gau --providers wayback example.com

---

## CommonCrawl Only

gau --providers commoncrawl example.com

---

## OTX Only

gau --providers otx example.com

---

## URLScan Only

gau --providers urlscan example.com

---

# FILTERING OPTIONS

## Filter Extensions

gau example.com --blacklist png,jpg,gif,css,svg

---

## Match Extensions

gau example.com --extensions php,aspx,jsp

---

## Remove Duplicates

gau example.com --fp

---

# OUTPUT OPTIONS

## JSON Output

gau example.com --json

---

## Save JSON Output

gau example.com --json > gau.json

---

## Output File

gau example.com -o urls.txt

---

# THREADING OPTIONS

## Set Threads

gau example.com --threads 50

---

## Timeout

gau example.com --timeout 30

---

# PARAMETER DISCOVERY

## Find URLs With Parameters

gau example.com | grep "="

---

## Extract XSS Candidates

gau example.com | gf xss

---

## Extract SQLi Candidates

gau example.com | gf sqli

---

# PIPELINE EXAMPLES

## GAU + HTTPX

gau example.com \
| httpx -silent

---

## GAU + GF

gau example.com \
| gf xss

---

## GAU + DALFOX

gau example.com \
| gf xss \
| dalfox pipe

---

## GAU + KATANA

gau example.com > gau_urls.txt

katana -list gau_urls.txt -silent

---

# URL CLEANING

## Remove Duplicate Parameters

gau example.com | uro

---

## Sort Unique

gau example.com | sort -u

---

# ADVANCED COMMANDS

## Fetch Subdomains Too

gau --subs example.com

---

## Include Only Parameters

gau example.com | grep "="

---

## Extract APIs

gau example.com | grep api

---

## Extract JS Files

gau example.com | grep ".js"

---

## Extract PHP Endpoints

gau example.com | grep ".php"

---

# RECON WORKFLOWS

## Historical Endpoint Discovery

gau example.com \
| tee gau_urls.txt

---

## XSS Recon Workflow

gau example.com \
| gf xss \
| dalfox pipe

---

## SQLi Recon Workflow

gau example.com \
| gf sqli

---

## LFI Recon Workflow

gau example.com \
| gf lfi

---

# AUTOMATION EXAMPLES

## Collect All URLs

gau example.com -o all_urls.txt

---

## Collect Parameters Only

gau example.com \
| grep "=" \
> params.txt

---

## Collect JS Endpoints

gau example.com \
| grep ".js" \
> js_files.txt

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| --subs | include subdomains |
| --providers | specify providers |
| --json | JSON output |
| --threads | concurrency |
| --timeout | timeout |
| --fp | remove duplicate params |
| --blacklist | exclude extensions |
| --extensions | include extensions |
| -o | output file |

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

GAU + GF is powerful for:
- XSS
- SQLi
- SSRF
- LFI

---

## Store Historical URLs

Useful for:
- bug bounty
- hidden endpoints
- deleted APIs

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

gau --subs example.com \
| uro \
| tee urls.txt

gf xss urls.txt

dalfox file urls.txt

---

# TROUBLESHOOTING

## Empty Results

Try:
--subs

or different providers.

---

## Slow Results

Reduce:
--threads

---

## Tool Not Found

Ensure:
- Go installed
- PATH configured

---

# HELP MENU

gau --help