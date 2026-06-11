# VAPT-Automated-Web-Enumeration-Toolkit
VAPT Automation Framework is a cross-platform reconnaissance automation tool for Windows, Linux, and macOS. It automates subdomain enumeration, URL discovery, parameter extraction, and directory scanning using multiple security tools. The framework provides live monitoring, output management, and organized reporting for efficient VAPT workflows.

# 🛡️ VAPT Automation Framework

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-orange?style=flat" alt="Platform">
  <img src="https://img.shields.io/badge/Version-2.0-red?style=flat" alt="Version">
</p>

<p align="center">
  <b>Cross-Platform Automated Reconnaissance & Vulnerability Assessment Engine</b>
</p>

---

# 🚀 Overview

The **VAPT Automation Framework** is a cross-platform reconnaissance automation platform designed to streamline the information gathering phase of Vulnerability Assessment and Penetration Testing (VAPT).

Instead of manually running multiple reconnaissance tools, the framework automates the complete workflow, organizes results, and generates structured outputs and reports.

The framework integrates multiple open-source security tools into a single pipeline for:

* ✅ Subdomain Enumeration
* ✅ Alive Host Discovery
* ✅ URL Discovery
* ✅ Parameter Discovery
* ✅ Pattern-Based Vulnerability Analysis
* ✅ Directory Enumeration
* ✅ Report Generation
* ✅ Output Management

---

# 🎯 Objectives

The primary objectives of this project are:

* Automate reconnaissance activities
* Reduce manual effort during penetration testing
* Improve efficiency and accuracy
* Standardize security assessment workflows
* Organize outputs automatically
* Support Windows, Linux, and macOS
* Generate structured reports for security analysts

---

# ✨ Features

## 🔧 Automated Tool Installation

Automatically installs required tools based on the operating system.

### Supported Platforms

* Windows
* Linux
* macOS

---

## ✅ Dependency Verification

Verifies:

* Installed tools
* Missing tools
* Runtime dependencies
* Platform compatibility

---

## ⚡ Automated Recon Workflow

Complete reconnaissance execution using a single framework.

```text
Target Domain
      │
      ▼
Subdomain Enumeration
      │
      ▼
Alive Host Discovery
      │
      ▼
URL Enumeration
      │
      ▼
Parameter Discovery
      │
      ▼
GF Pattern Analysis
      │
      ▼
Directory Enumeration
      │
      ▼
Report Generation
```

---

## 🌎 Cross Platform Support

Supports:

* Windows
* Linux
* macOS

with platform-specific installation and execution handling.

---

# 🏗️ Architecture

```text
                    User
                      │
                      ▼
                  main.py
                      │
                      ▼
               Workflow Engine
                      │
     ┌──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼
Dependency   Installer   Recon      Logger
 Checker                Engine
                      │
                      ▼
               Recon Pipeline
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Subdomains       Alive Hosts        URLs
      │               │               │
      ▼               ▼               ▼
 Parameters      GF Analysis     Directories
                      │
                      ▼
                Report Engine
                      │
                      ▼
                  Outputs
```

---

# 🔍 Reconnaissance Pipeline

## Phase 1 – Subdomain Enumeration

### Tools

* Subfinder
* Assetfinder
* Amass
* Findomain
* GitHub Subdomains
* Subscraper

### Purpose

Discover all possible subdomains associated with the target.

### Example

```text
api.target.com
mail.target.com
dev.target.com
```

---

## Phase 2 – Alive Host Discovery

### Tool

* HTTPX

### Purpose

Identify active and reachable hosts.

### Example

```text
https://api.target.com
https://dev.target.com
```

---

## Phase 3 – URL Enumeration

### Tools

* Gau
* Waybackurls
* Katana

### Purpose

Discover archived, historical, and crawled URLs.

### Example

```text
/administrator
/api/users
/profile
/login
```

---

## Phase 4 – Parameter Discovery

### Tools

* ParamSpider
* Arjun

### Purpose

Identify parameters useful for security testing.

### Example

```text
?id=
?user=
?token=
?redirect=
```

---

## Phase 5 – GF Pattern Analysis

### Tool

* GF

### Patterns

* XSS
* SQL Injection
* SSRF
* LFI
* RCE
* IDOR
* Open Redirect
* Debug Logic

### Purpose

Identify potentially vulnerable URLs.

---

## Phase 6 – Directory Enumeration

### Tools

* FFUF
* Dirsearch

### Purpose

Discover hidden directories and files.

### Example

```text
/admin
/uploads
/backup
/config
```

---

# ⚙️ Technologies Used

## Programming Languages

### Python

Used for:

* Workflow Automation
* Tool Execution
* Parsing
* Validation
* Reporting
* Logging
* Output Management

### Go (Golang)

Used by:

* Subfinder
* Assetfinder
* HTTPX
* Gau
* Katana
* Waybackurls
* GF
* FFUF
* GitHub Subdomains

### Rust

Used by:

* Findomain
* Feroxbuster (Optional)

---

## Core Python Libraries

```text
asyncio
subprocess
pathlib
json
re
shutil
platform
typing
```

---

# 🧠 Algorithms Used

## Subdomain Enumeration Algorithm

Collects subdomains from:

* DNS Records
* Certificate Transparency Logs
* Search Engines
* GitHub Repositories
* OSINT Sources

---

## DNS & OSINT Discovery

Uses publicly available intelligence sources to discover attack surfaces.

---

## Deduplication Algorithm

Uses set-based filtering:

```python
set(results)
```

Purpose:

Remove duplicate entries collected from multiple tools.

---

## HTTP Alive Host Detection Algorithm

Process:

```text
Send Request
Receive Response
Validate Status Code
```

Used to identify active hosts.

---

## URL Crawling Algorithm

Implemented through Katana.

Works similarly to BFS-style traversal for discovering new URLs.

---

## Regex Pattern Matching

Used for extracting:

* URLs
* Domains
* Parameters
* Emails

from raw outputs.

---

## Parameter Extraction Algorithm

Identifies:

```text
id
user
token
redirect
```

for further security testing.

---

## Directory Bruteforce Algorithm

Used by:

* FFUF
* Dirsearch

Purpose:

Discover hidden resources using wordlists.

---

## Validation & Scope Filtering

Removes:

* Invalid URLs
* Duplicate Results
* Out-of-Scope Assets

---

## Pipeline Processing Workflow

Output of one phase becomes the input of the next phase.

---

## Asynchronous Task Scheduling

Implemented using:

```python
asyncio
```

Benefits:

* Faster execution
* Better resource utilization
* Non-blocking operations

---

# 🛠️ Tools Integrated

## Subdomain Enumeration

```text
subfinder
assetfinder
amass
findomain
github-subdomains
subscraper
```

## Alive Host Discovery

```text
httpx
```

## URL Enumeration

```text
gau
waybackurls
katana
```

## Parameter Discovery

```text
paramspider
arjun
```

## Pattern Analysis

```text
gf
```

## Directory Enumeration

```text
ffuf
dirsearch
```

---

# 📂 Project Structure

```text
VAPT-Automation-Framework/
│
├── core/
│   ├── dependency_checker.py
│   ├── executor.py
│   ├── logger.py
│   ├── output_manager.py
│   ├── parser.py
│   ├── recon_engine.py
│   ├── recon_engine_async.py
│   ├── tool_installer.py
│   ├── tool_registry.py
│   ├── validator.py
│   └── workflow_engine.py
│
├── installers/
│   ├── windows/
│   ├── linux/
│   └── macos/
│
├── tools/
├── outputs/
├── wordlists/
├── reports/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 📊 Output Structure

```text
outputs/
└── scans/
    └── target.com/
        │
        ├── subdomains/
        ├── httpx/
        ├── urls/
        ├── parameters/
        ├── gf_patterns/
        ├── directories/
        ├── reports/
        ├── metadata/
        └── logs/
```

---

# 💻 Installation

## Clone Repository

```bash
git clone https://github.com/pranoti711/VAPT-Automation-Framework.git
cd VAPT-Automation-Framework
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Framework

```bash
python main.py
```

---

# 🚀 Usage

Start the framework:

```bash
python main.py
```

### Menu

```text
1. Install Tools
2. Check Tools
3. Run Recon Scan
4. Clean Outputs
5. Export Reports
6. Backup Outputs
7. Update Tools
8. Show Environment
9. Show System Info
10. Launch Interactive CLI
0. Exit
```

---

# 📈 Sample Workflow

```text
Target: example.com

Subdomains Found: 4,213
Alive Hosts: 385
URLs Discovered: 21,456
Parameters Found: 1,532
GF Findings: 647
Directories Found: 234
```

---

# 🔒 Security Notice

This framework is intended only for:

* Authorized Security Testing
* Educational Purposes
* Research Environments
* Bug Bounty Programs

Always obtain proper authorization before testing any target.

---

# 🚀 Future Enhancements

* Nuclei Integration
* Screenshot Capture
* Technology Fingerprinting
* AI-Based Risk Scoring
* PDF Report Generation
* Distributed Scanning
* Vulnerability Verification Engine
* Web Dashboard

---

# 👩‍💻 Author

**Pranoti Ashok Munjankar**

Cyber Security Researcher | Security Automation Developer

GitHub: https://github.com/pranoti711

---

# 📄 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgements

Special thanks to:

* ProjectDiscovery
* OWASP Amass
* Tomnomnom
* FFUF
* Dirsearch
* Arjun
* ParamSpider
* M8sec Subscraper
* Open Source Security Community

---

<div align="center">

### ⭐ If you found this project useful, please consider giving it a star!

**VAPT Automation Framework — Automating Reconnaissance for Faster Security Assessments.**

</div>
