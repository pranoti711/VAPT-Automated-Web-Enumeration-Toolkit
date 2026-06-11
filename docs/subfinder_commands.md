# Subfinder Commands

## Basic Enumeration

subfinder -d example.com

## Silent Mode

subfinder -d example.com -silent

## Save Output

subfinder -d example.com -o subs.txt

## Use Config

subfinder -d example.com -config config.yaml

## Multiple Domains

subfinder -dL domains.txt

## Recursive Enumeration

subfinder -d example.com -recursive

## Use Specific Sources

subfinder -d example.com -sources crtsh,virustotal

## Exclude Sources

subfinder -d example.com -exclude-sources censys

## Rate Limit

subfinder -d example.com -rl 10

## JSON Output

subfinder -d example.com -oJ

## Verbose Mode

subfinder -d example.com -v

## All Sources

subfinder -d example.com -all