# Katana Commands

## About

Katana is a fast web crawler developed by ProjectDiscovery.

Used for:
- crawling websites
- endpoint discovery
- JavaScript endpoint extraction
- URL harvesting
- attack surface mapping

Repository:
https://github.com/projectdiscovery/katana

---

# BASIC COMMANDS

## Crawl Single Target

katana -u https://example.com

---

## Silent Mode

katana -u https://example.com -silent

---

## Save Output

katana -u https://example.com -o katana.txt

---

## Crawl Multiple Targets

katana -list targets.txt

---

# DEPTH OPTIONS

## Set Crawl Depth

katana -u https://example.com -d 5

---

## Unlimited Depth

katana -u https://example.com -d 10

---

# JAVASCRIPT CRAWLING

## Enable JavaScript Crawling

katana -u https://example.com -jc

---

## Extract JavaScript Files

katana -u https://example.com -js-crawl

---

## Parse JavaScript Endpoints

katana -u https://example.com -jsluice

---

# HEADLESS MODE

## Enable Headless Browser Crawling

katana -u https://example.com -headless

---

## Chrome Headless With System Chrome

katana -u https://example.com -system-chrome

---

## Headless With No Sandbox

katana -u https://example.com -headless -no-sandbox

---

# RATE LIMITING

## Set Rate Limit

katana -u https://example.com -rl 50

---

## Set Concurrency

katana -u https://example.com -c 20

---

## Parallelism

katana -u https://example.com -p 10

---

# FORM OPTIONS

## Crawl Forms

katana -u https://example.com -forms

---

## Automatic Form Filling

katana -u https://example.com -automatic-form-fill

---

# OUTPUT OPTIONS

## JSON Output

katana -u https://example.com -jsonl

---

## Store Responses

katana -u https://example.com -store-response

---

## Response Directory

katana -u https://example.com -store-response-dir responses/

---

# FILTER OPTIONS

## Match Regex

katana -u https://example.com -mr login

---

## Filter Regex

katana -u https://example.com -fr logout

---

## Match Extension

katana -u https://example.com -em php,aspx,jsp

---

## Filter Extension

katana -u https://example.com -ef png,jpg,gif

---

# SCOPE OPTIONS

## Restrict To Domain

katana -u https://example.com -fs dn

---

## Restrict To Host

katana -u https://example.com -fs fqdn

---

## Scope Regex

katana -u https://example.com -cs login

---

# CUSTOM HEADERS

## Add Header

katana -u https://example.com -H "Authorization: Bearer token"

---

## Custom User-Agent

katana -u https://example.com -H "User-Agent: Mozilla"

---

# COOKIE OPTIONS

## Add Cookies

katana -u https://example.com -H "Cookie: session=abcd"

---

# PROXY OPTIONS

## Use Proxy

katana -u https://example.com -proxy http://127.0.0.1:8080

---

## SOCKS5 Proxy

katana -u https://example.com -proxy socks5://127.0.0.1:9050

---

# AUTHENTICATION

## Basic Authentication

katana -u https://example.com -H "Authorization: Basic base64"

---

# AUTOMATION PIPELINES

## Crawl Alive Hosts

httpx -l alive.txt -silent | katana -silent

---

## Save Crawled URLs

katana -list alive.txt -silent -o urls.txt

---

## Crawl + GF

katana -u https://example.com -silent | gf xss

---

## Crawl + Dalfox

katana -u https://example.com -silent | gf xss | dalfox pipe

---

# ADVANCED COMMANDS

## Ignore Query Parameters

katana -u https://example.com -iqp

---

## Ignore Redirects

katana -u https://example.com -disable-redirects

---

## Crawl Known Files

katana -u https://example.com -kf all

---

## Known Files Deep Crawl

katana -u https://example.com -kf robotstxt,sitemapxml

---

## Extract Forms

katana -u https://example.com -fx

---

## Passive Crawling

katana -u https://example.com -passive

---

# URL EXTRACTION

## Extract Parameters

katana -u https://example.com -silent | grep "="

---

## Extract API Endpoints

katana -u https://example.com -mr api

---

# JSON EXAMPLES

## JSON Output To File

katana -u https://example.com -jsonl -o output.json

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -u | target URL |
| -list | input list |
| -silent | silent mode |
| -jc | JS crawling |
| -jsluice | parse JS |
| -headless | browser crawling |
| -d | depth |
| -c | concurrency |
| -p | parallelism |
| -rl | rate limit |
| -jsonl | JSON output |
| -o | output file |
| -proxy | proxy |
| -H | custom header |
| -forms | form crawling |
| -store-response | save responses |

---

# BEST PRACTICES

## Use Silent Mode In Pipelines

katana -silent

Prevents unnecessary output.

---

## Combine With HTTPX

httpx → katana

Only crawl alive targets.

---

## Enable JS Crawling

Modern apps heavily depend on JavaScript.

---

## Save Responses

Useful for:
- screenshots
- manual analysis
- debugging

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

katana -list alive.txt -silent -jc -o urls.txt

gf xss urls.txt

dalfox file xss.txt

---

# TROUBLESHOOTING

## Chrome Errors

Install Chrome or use:
-system-chrome

---

## Headless Crashes

Use:
-no-sandbox

---

## Tool Not Found

Ensure:
- Go installed
- GOPATH configured
- PATH updated

---

# HELP MENU

katana -h