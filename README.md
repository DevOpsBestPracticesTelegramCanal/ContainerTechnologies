# Container Technologies Databases

> Comprehensive SQLite databases for container technologies: releases, news, and CVE vulnerabilities

[![Downloads](https://img.shields.io/badge/downloads-via_telegram-blue)](https://t.me/devopsbestpractices_bot)
[![Channel](https://img.shields.io/badge/telegram-@devops__best__practices-blue)](https://t.me/devops_best_practices)
[![Data Period](https://img.shields.io/badge/period-Jan--Nov_2025-green)]()

## Overview

Three curated SQLite databases with verified data about container technologies, cloud-native platforms, and security vulnerabilities:

| Database | Records | Period | Description |
|----------|---------|--------|-------------|
| **releases_database.db** | 542 | Jan-Nov 2025 | Container technology releases |
| **news_database.db** | 219 | Jan-Nov 2025 | Curated industry news |
| **cve_database.db** | 343 | 2020-2025 | CVE vulnerabilities + affected projects |

**Key Features:**
- ✅ 100% active links verified
- ✅ Russian annotations for all records
- ✅ All table columns filled (95-100%)
- ✅ Ready for immediate use

## Quick Start

### Option 1: Download via Telegram Bot (Recommended)

1. Subscribe to [@devops_best_practices](https://t.me/devops_best_practices)
2. Message [@devopsbestpractices_bot](https://t.me/devopsbestpractices_bot)
3. Use command: `/get_database`
4. Receive all 3 databases instantly

**Limits:** 5 downloads per day per user

### Option 2: Clone from GitHub

```bash
git clone https://github.com/DevOpsBestPracticesTelegramCanal/ContainerTechnologies.git
cd ContainerTechnologies
```

## Database Contents

### 1. Releases Database (542 records)

Container technology releases from major projects:

- **Kubernetes** - 107 releases
- **Docker** - 104 releases
- **Podman** - 31 releases
- **containerd**, **runc**, **CRI-O** - 58 releases
- **Monitoring tools** (Prometheus, Grafana) - 40 releases
- **Other projects** - 202 releases

**Fields:** version, release_url, description, has_security_fix, importance_score, title_ru, annotation_ru, published_date, etc.

### 2. News Database (219 records)

Curated news articles from authoritative sources:

**Categories:**
- Kubernetes (85 articles)
- Docker (52 articles)
- Security (34 articles)
- Monitoring (28 articles)
- Service Mesh, WebAssembly, Edge (20 articles)

**Sources:**
- Kubernetes Blog
- Docker Blog
- Dev.to
- GitHub Releases

**Fields:** title, link, description, category, importance, keywords, title_ru, annotation_ru, pub_date, etc.

### 3. CVE Database (343 vulnerabilities)

Comprehensive vulnerability data with intelligent scoring:

**Coverage:**
- **Total CVE:** 343
- **With Affected Projects:** 268 (78.1%)
- **With Public Exploits:** 38 (11.1%)
- **Severity:** 16 CRITICAL, 81 HIGH, 156 MEDIUM, 90 LOW

**Top Affected Projects:**
- Kubernetes - 107 CVE
- Docker - 104 CVE
- Podman - 31 CVE
- Jenkins - 22 CVE
- runc - 21 CVE

**Data Sources:**
- NVD (NIST) - 314 CVE
- GitHub Security Advisory - 28 CVE
- OSV - 1 CVE

**Features:**
- Intelligent scoring system (platform-aware priority)
- CVE-to-project mappings
- Exploit availability tracking
- 6,051 external references

**Fields:** cve_id, title, cvss_score, cvss_severity, intelligent_score, affected_projects, exploits, references, etc.

## Usage Examples

### Using SQLite Command Line

```bash
# Open database
sqlite3 data/releases_database.db

# View tables
.tables

# Query releases
SELECT project_id, version, published_at
FROM releases
WHERE has_security_fix = 1
ORDER BY importance_score DESC
LIMIT 10;

# Exit
.quit
```

### Using Python

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('data/releases_database.db')
cursor = conn.cursor()

# Get Kubernetes releases
cursor.execute('''
    SELECT version, published_at, annotation_ru
    FROM releases
    WHERE project_id = 'kubernetes'
    ORDER BY published_at DESC
    LIMIT 5
''')

for row in cursor.fetchall():
    print(row)

conn.close()
```

### Using GUI Tools

**Recommended:** [DB Browser for SQLite](https://sqlitebrowser.org/)
1. Download and install
2. Open Database → select .db file
3. Browse data visually

## Documentation

- **[КАК_РАБОТАТЬ_С_SQLITE.md](./КАК_РАБОТАТЬ_С_SQLITE.md)** - Complete SQLite tutorial (Russian)
- **[README_CVE_DATABASE.md](./README_CVE_DATABASE.md)** - CVE database detailed docs
- **[СИСТЕМА_ГОТОВА_К_ИСПОЛЬЗОВАНИЮ.md](./СИСТЕМА_ГОТОВА_К_ИСПОЛЬЗОВАНИЮ.md)** - System overview (Russian)

## Statistics

**Data Quality:**
- 📊 1,104 total records (542 + 219 + 343)
- 🌍 100% Russian localization
- 🔗 100% active links verified
- 📅 Complete coverage Jan-Nov 2025

**File Sizes:**
- releases_database.db - 3.2 MB
- news_database.db - 1.8 MB
- cve_database.db - 2.5 MB
- **Total:** ~7.5 MB

## Access Control

### Via Telegram Bot

**Requirements:**
- ✅ Subscription to [@devops_best_practices](https://t.me/devops_best_practices)
- ✅ Daily limit: 5 downloads per user
- ✅ All downloads logged

**Commands:**
- `/get_database` - Download all databases
- `/my_stats` - View your download statistics
- `/help` - Bot help

### Via GitHub

**Free access:** Clone this repository anytime
```bash
git clone https://github.com/DevOpsBestPracticesTelegramCanal/ContainerTechnologies.git
```

## Updates

Databases are updated regularly:
- **Releases:** Weekly (new container technology releases)
- **News:** Weekly (curated articles)
- **CVE:** Daily (new vulnerabilities)

Subscribe to [@devops_best_practices](https://t.me/devops_best_practices) for update notifications.

## Use Cases

**For DevOps Engineers:**
- Track container technology releases
- Monitor security vulnerabilities
- Plan upgrades and patches

**For Security Teams:**
- CVE vulnerability database
- Affected projects mapping
- Exploit availability tracking

**For Content Creators:**
- News aggregation source
- Release announcement tracking
- Industry trends analysis

**For Researchers:**
- Historical data analysis
- Trend identification
- Academic research

## Technology Stack

- **Database:** SQLite 3
- **Data Sources:** 50+ authoritative sources
- **Collection:** Automated Python scripts
- **Verification:** 100% link checking
- **Localization:** Automated Russian translations

## Contributing

Found an issue or want to suggest improvements?
- Open an issue on GitHub
- Contact us on [Telegram](https://t.me/devops_best_practices)

## License

Databases aggregate publicly available data from:
- NVD (NIST) - Public Domain
- GitHub - Community Data
- Kubernetes Blog - Apache 2.0
- Docker Blog - Creative Commons

Collection scripts and enhancements: Provided as-is for research purposes.

## Credits

**Data Sources:**
- [NIST National Vulnerability Database](https://nvd.nist.gov/)
- [GitHub Security Advisory](https://github.com/advisories)
- [Kubernetes Blog](https://kubernetes.io/blog/)
- [Docker Blog](https://www.docker.com/blog/)

**Telegram:**
- Channel: [@devops_best_practices](https://t.me/devops_best_practices)
- Bot: [@devopsbestpractices_bot](https://t.me/devopsbestpractices_bot)

---

**Last Updated:** November 11, 2025
**Version:** 1.0
**Status:** ✅ Production Ready
