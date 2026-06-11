# FFUF Commands

## About

FFUF (Fuzz Faster U Fool) is used for:
- directory brute forcing
- file discovery
- parameter fuzzing
- virtual host fuzzing
- API fuzzing
- hidden endpoint discovery

Repository:
https://github.com/ffuf/ffuf

---

# BASIC COMMANDS

## Directory Enumeration

ffuf -u https://example.com/FUZZ -w wordlist.txt

---

## File Enumeration

ffuf -u https://example.com/FUZZ.php -w wordlist.txt

---

## Save Output

ffuf -u https://example.com/FUZZ -w wordlist.txt -o output.json

---

## Silent Mode

ffuf -u https://example.com/FUZZ -w wordlist.txt -s

---

# WORDLIST OPTIONS

## Use Single Wordlist

ffuf -u https://example.com/FUZZ -w wordlist.txt

---

## Multiple Wordlists

ffuf -u https://FUZZ.example.com/W1 -w subdomains.txt:FUZZ -w paths.txt:W1

---

# FILTERING OPTIONS

## Match Status Codes

ffuf -u https://example.com/FUZZ -w wordlist.txt -mc 200,301,302

---

## Filter Status Codes

ffuf -u https://example.com/FUZZ -w wordlist.txt -fc 404

---

## Match Content Length

ffuf -u https://example.com/FUZZ -w wordlist.txt -ms 100

---

## Filter Content Length

ffuf -u https://example.com/FUZZ -w wordlist.txt -fs 0

---

## Match Words

ffuf -u https://example.com/FUZZ -w wordlist.txt -mw 10

---

## Filter Words

ffuf -u https://example.com/FUZZ -w wordlist.txt -fw 0

---

## Match Regex

ffuf -u https://example.com/FUZZ -w wordlist.txt -mr admin

---

## Filter Regex

ffuf -u https://example.com/FUZZ -w wordlist.txt -fr error

---

# RECURSIVE FUZZING

## Enable Recursion

ffuf -u https://example.com/FUZZ -w wordlist.txt -recursion

---

## Recursive Depth

ffuf -u https://example.com/FUZZ -w wordlist.txt -recursion-depth 3

---

# THREADS & SPEED

## Set Threads

ffuf -u https://example.com/FUZZ -w wordlist.txt -t 100

---

## Rate Limiting

ffuf -u https://example.com/FUZZ -w wordlist.txt -rate 50

---

## Timeout

ffuf -u https://example.com/FUZZ -w wordlist.txt -timeout 10

---

# EXTENSIONS

## Add Extensions

ffuf -u https://example.com/FUZZ -w wordlist.txt -e .php,.txt,.bak

---

## Backup File Discovery

ffuf -u https://example.com/FUZZ -w wordlist.txt -e .zip,.bak,.old

---

# OUTPUT OPTIONS

## JSON Output

ffuf -u https://example.com/FUZZ -w wordlist.txt -of json -o results.json

---

## HTML Output

ffuf -u https://example.com/FUZZ -w wordlist.txt -of html -o report.html

---

## CSV Output

ffuf -u https://example.com/FUZZ -w wordlist.txt -of csv -o report.csv

---

# HEADER OPTIONS

## Custom Header

ffuf -u https://example.com/FUZZ -w wordlist.txt -H "Authorization: Bearer token"

---

## Custom User-Agent

ffuf -u https://example.com/FUZZ -w wordlist.txt -H "User-Agent: Mozilla"

---

## Cookies

ffuf -u https://example.com/FUZZ -w wordlist.txt -b "session=abcd"

---

# HTTP METHODS

## POST Request

ffuf -X POST -u https://example.com/FUZZ -w wordlist.txt

---

## PUT Request

ffuf -X PUT -u https://example.com/FUZZ -w wordlist.txt

---

# POST DATA FUZZING

## POST Body Fuzzing

ffuf -X POST \
-u https://example.com/login \
-d "username=admin&password=FUZZ" \
-w passwords.txt

---

# PARAMETER FUZZING

## GET Parameter Fuzzing

ffuf -u "https://example.com/page.php?id=FUZZ" -w ids.txt

---

## POST Parameter Fuzzing

ffuf -X POST \
-u https://example.com/login \
-d "user=admin&pass=FUZZ" \
-w passwords.txt

---

# SUBDOMAIN FUZZING

## Virtual Host Discovery

ffuf -u https://example.com \
-H "Host: FUZZ.example.com" \
-w subdomains.txt

---

## HTTPS VHOST Fuzzing

ffuf -u https://target.com \
-H "Host: FUZZ.target.com" \
-w subdomains.txt

---

# API FUZZING

## API Endpoint Discovery

ffuf -u https://api.example.com/FUZZ -w api.txt

---

## REST API Enumeration

ffuf -X GET \
-u https://api.example.com/FUZZ \
-w endpoints.txt

---

# REPLAY PROXY

## Burp Suite Proxy

ffuf -u https://example.com/FUZZ \
-w wordlist.txt \
-replay-proxy http://127.0.0.1:8080

---

# AUTOMATION EXAMPLES

## Directory Bruteforce

ffuf -u https://example.com/FUZZ \
-w common.txt \
-mc 200,301,302

---

## Hidden Admin Discovery

ffuf -u https://example.com/FUZZ \
-w admin.txt \
-fr "404"

---

## API Enumeration

ffuf -u https://api.example.com/FUZZ \
-w api.txt \
-of json \
-o api.json

---

# PIPELINE EXAMPLES

## HTTPX + FFUF

httpx -l alive.txt -silent \
| ffuf -u FUZZ/admin -w dirs.txt

---

## Katana + FFUF

katana -u https://example.com -silent \
| ffuf -u FUZZ -w dirs.txt

---

# ADVANCED OPTIONS

## Auto Calibration

ffuf -u https://example.com/FUZZ -w wordlist.txt -ac

---

## Stop On Errors

ffuf -u https://example.com/FUZZ -w wordlist.txt -se

---

## Follow Redirects

ffuf -u https://example.com/FUZZ -w wordlist.txt -r

---

## Delay Between Requests

ffuf -u https://example.com/FUZZ -w wordlist.txt -p 0.5

---

# COMMON FLAGS

| Flag | Description |
|------|-------------|
| -u | target URL |
| -w | wordlist |
| -mc | match codes |
| -fc | filter codes |
| -fs | filter size |
| -fw | filter words |
| -mr | match regex |
| -fr | filter regex |
| -recursion | recursive fuzzing |
| -t | threads |
| -rate | rate limit |
| -timeout | timeout |
| -e | extensions |
| -H | header |
| -b | cookies |
| -X | request method |
| -d | POST data |
| -o | output |
| -of | output format |

---

# BEST PRACTICES

## Use Auto Calibration

-ac

Reduces false positives.

---

## Use Filters

Filter:
- 404
- redirects
- identical responses

---

## Use Rate Limiting

Avoid bans/WAF detection.

---

## Use Replay Proxy

Useful with Burp Suite.

---

# COMPLETE RECON EXAMPLE

subfinder -d example.com -silent -o subs.txt

httpx -l subs.txt -silent -o alive.txt

ffuf -u https://example.com/FUZZ \
-w common.txt \
-mc 200,301,302 \
-o ffuf.json

---

# TROUBLESHOOTING

## False Positives

Use:
-ac
-fs
-fw

---

## Tool Not Found

Ensure:
- Go installed
- PATH updated

---

## Too Many Requests

Reduce:
-rate
-t

---

# HELP MENU

ffuf -h