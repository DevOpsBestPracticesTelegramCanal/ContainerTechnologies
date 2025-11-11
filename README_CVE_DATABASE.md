# Container Technologies CVE Database

> Comprehensive vulnerability database for container technologies and cloud-native platforms

## Overview

This database provides curated CVE (Common Vulnerabilities and Exposures) information specifically focused on container technologies, orchestration platforms, and cloud-native infrastructure. The data is collected from multiple authoritative sources, enriched with intelligent scoring, and mapped to specific projects and releases.

## Database Statistics

**Last Updated:** November 11, 2025

### Coverage Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total CVE** | 343 | 100% |
| **With Affected Projects** | 268 | 78.1% |
| **With Exploits** | 38 | 11.1% |
| **With Intelligent Score** | 343 | 100% |
| **With Russian Translations** | 0 | 0.0% |

### Data Sources

| Source | CVE Count | Description |
|--------|-----------|-------------|
| **NVD** | 314 | National Vulnerability Database (NIST) |
| **GitHub Security Advisory** | 28 | GitHub Advisory Database |
| **OSV** | 1 | Open Source Vulnerabilities |

### Top Affected Projects

| Rank | Project | CVE Count | Category |
|------|---------|-----------|----------|
| 1 | Kubernetes | 107 | Orchestration |
| 2 | Docker | 104 | Container Runtime |
| 3 | Podman | 31 | Container Runtime |
| 4 | Jenkins | 22 | CI/CD |
| 5 | runc | 21 | Container Runtime |
| 6 | CRI-O | 19 | Container Runtime |
| 7 | containerd | 18 | Container Runtime |
| 8 | Registry | 13 | Image Distribution |
| 9 | OpenShift | 11 | Platform |
| 10 | GitLab | 9 | DevOps Platform |

**Additional Projects Tracked:** kubectl, Apache, Helm, Moby, NGINX, Buildah, crun, Distribution, kind, and 22 more...

## Database Structure

### 1. CVE Vulnerabilities (`cve_vulnerabilities`)

Main table containing vulnerability information:

- **cve_id**: CVE identifier (e.g., CVE-2024-1234)
- **title**: Brief description
- **description**: Detailed vulnerability description
- **cvss_score**: CVSS v3 score (0-10)
- **cvss_severity**: Severity level (CRITICAL/HIGH/MEDIUM/LOW)
- **cvss_vector**: CVSS vector string
- **published_date**: Publication date
- **source**: Data source (NVD, GitHub, OSV)
- **intelligent_score**: Calculated priority score
- **risk_level**: Risk classification
- **title_ru**: Russian translation (if available)
- **description_ru**: Russian description (if available)

### 2. Affected Projects (`cve_affected_projects`)

CVE-to-project mappings:

- **cve_id**: Reference to CVE
- **project_name**: Affected project/product
- **vendor**: Vendor name
- **product**: Product name
- **affected_versions**: Vulnerable versions
- **fixed_in_version**: Fix version
- **is_fixed**: Fix status

**Total Records:** 425 mappings
**Unique CVE:** 268 (78.1% coverage)
**Unique Projects:** 42

### 3. Exploits (`cve_exploits`)

Public exploit information:

- **cve_id**: Reference to CVE
- **exploit_exists**: Boolean flag
- **exploit_url**: Link to exploit code/PoC
- **exploit_description**: Exploit details

**Total Exploits:** 38 (11.1% of CVE)

### 4. References (`cve_references`)

External references and resources:

- **cve_id**: Reference to CVE
- **url**: Reference URL
- **reference_type**: Type (Advisory, Issue, Patch, etc.)
- **title**: Reference title
- **source**: Reference source

**Total References:** 6,051 links

## Intelligent Scoring System

Each CVE is assigned an intelligent priority score using the formula:

```
Score = CVSS × Platform_Priority × (1 + Exploit_Bonus + BDU_Bonus)
```

### Platform Priorities

- **Kubernetes**: 2.0 (highest priority)
- **Docker**: 1.8
- **containerd**: 1.7
- **runc**: 1.7
- **CRI-O**: 1.6
- **Podman**: 1.5
- **Other platforms**: 1.0-1.3

### Bonuses

- **Exploit Available**: +2.0 multiplier (public exploit exists)
- **BDU FSTEC**: +1.0 multiplier (in Russian vulnerability database)

### Example Calculations

**Critical Priority CVE:**
```
CVE-2024-1234 (Kubernetes privilege escalation)
CVSS: 9.8 × Platform: 2.0 × (1 + Exploit: 2.0) = Score: 58.8
→ Risk Level: CRITICAL
```

**High Priority CVE:**
```
CVE-2024-5678 (Docker container escape)
CVSS: 8.1 × Platform: 1.8 × (1 + 0) = Score: 14.6
→ Risk Level: HIGH
```

## Exported Data Files

All data is available in JSON format:

1. **cve_vulnerabilities_YYYYMMDD_HHMMSS.json** (364 KB)
   - Complete CVE vulnerability data
   - 343 records

2. **cve_affected_projects_YYYYMMDD_HHMMSS.json** (86 KB)
   - CVE-to-project mappings
   - 425 records

3. **cve_exploits_YYYYMMDD_HHMMSS.json** (11 KB)
   - Public exploit information
   - 38 records

4. **cve_references_YYYYMMDD_HHMMSS.json** (1.3 MB)
   - External references
   - 6,051 records (top 10,000 limit)

5. **export_summary_YYYYMMDD_HHMMSS.json** (2 KB)
   - Complete statistics
   - Source breakdown
   - Top projects list

## Usage Examples

### Query CVE by Project

```python
import sqlite3
import json

conn = sqlite3.connect('data/cve_database.db')
c = conn.cursor()

# Get all Kubernetes CVE
c.execute('''
    SELECT DISTINCT v.cve_id, v.title, v.cvss_score, v.intelligent_score
    FROM cve_vulnerabilities v
    JOIN cve_affected_projects ap ON v.cve_id = ap.cve_id
    WHERE ap.project_name = 'kubernetes'
    ORDER BY v.intelligent_score DESC
''')

for row in c.fetchall():
    print(f"{row[0]}: {row[1]} (CVSS: {row[2]}, Score: {row[3]})")
```

### Find High-Priority CVE with Exploits

```python
c.execute('''
    SELECT v.cve_id, v.title, v.cvss_score, v.intelligent_score
    FROM cve_vulnerabilities v
    JOIN cve_exploits e ON v.cve_id = e.cve_id
    WHERE v.intelligent_score > 20 AND e.exploit_exists = 1
    ORDER BY v.intelligent_score DESC
''')
```

### Search by Severity

```python
c.execute('''
    SELECT cve_id, title, cvss_score, intelligent_score
    FROM cve_vulnerabilities
    WHERE cvss_severity = 'CRITICAL'
    ORDER BY intelligent_score DESC
''')
```

## Data Collection Process

### Collectors Implemented

1. **NVD Collector** (`collect_nvd_api.py`)
   - National Vulnerability Database API v2.0
   - Filtered by container-related keywords
   - Enhanced CPE analysis
   - Result: 314 CVE

2. **GitHub Security Advisory** (`collect_github_advisories.py`)
   - GitHub Advisory Database API
   - Container ecosystem packages
   - Result: 28 CVE

3. **OSV Collector** (`collect_osv_vulnerabilities.py`)
   - Open Source Vulnerabilities database
   - Container runtime packages
   - Result: 1 CVE

4. **Affected Projects Enhancer** (`enhance_affected_projects.py`)
   - 221 regex patterns for 73+ projects
   - Text analysis of CVE descriptions
   - Confidence scoring (0.85-0.95)
   - Result: 78.1% coverage (up from 2.6%)

5. **Intelligent Scoring** (`intelligent_scoring_system.py`)
   - Platform-aware priority calculation
   - Exploit bonus integration
   - Result: All 343 CVE scored

### Additional Collectors (Available but Not Run)

- **БДУ ФСТЭК** (`collect_fstec_bdu_v3.py`) - Russian vulnerability database
- **Vulners.com** (`collect_vulners_api.py`) - Russian translations, requires API key
- **Red Hat Security** (`collect_redhat_security.py`) - RHEL/OpenShift advisories

## Integration with Releases Database

The CVE database is linked to `releases_database.db` containing:

- **648 releases** tracked across container projects
- **362 CVE-to-release links** automatically detected
- Release version correlation with vulnerability data

## Coverage Analysis

### By Severity

| Severity | Count | With Projects | Coverage |
|----------|-------|---------------|----------|
| CRITICAL | 16 | 14 | 87.5% |
| HIGH | 81 | 77 | 95.1% |
| MEDIUM | 156 | 115 | 73.7% |
| LOW | 90 | 62 | 68.9% |

### By Project Category

| Category | Projects | CVE Count | Avg Score |
|----------|----------|-----------|-----------|
| **Orchestration** | 4 | 130 | 12.5 |
| **Container Runtime** | 8 | 197 | 11.8 |
| **CI/CD** | 3 | 31 | 10.2 |
| **Image Distribution** | 2 | 16 | 9.7 |
| **Networking** | 3 | 12 | 8.9 |
| **Monitoring** | 2 | 8 | 7.4 |

## Known Limitations

1. **Russian Translations**: 0% coverage
   - **Reason**: БДУ ФСТЭК site accessibility issues, Vulners.com requires API key
   - **Solution**: Manual XLSX import or API key registration

2. **Exploit Coverage**: 11.1%
   - **Reason**: Only public exploits from Exploit-DB currently tracked
   - **Enhancement**: Add Metasploit, PacketStorm, GitHub PoCs

3. **Historical Data**: Limited to recent CVE
   - **Current**: Primarily 2020-2024
   - **Enhancement**: Backfill older vulnerabilities

## Future Enhancements

### Phase 1: Data Quality (Priority: HIGH)
- [ ] Add БДУ ФСТЭК Russian translations (target: +120 CVE)
- [ ] Integrate Vulners.com API for more translations
- [ ] Enhance exploit detection from GitHub repositories
- [ ] Add Metasploit module tracking

### Phase 2: Additional Sources (Priority: MEDIUM)
- [ ] Red Hat Security Advisory (RHSA)
- [ ] Ubuntu Security Notices (USN)
- [ ] Debian Security Tracker
- [ ] SUSE Security Updates
- [ ] Alpine Linux Security

### Phase 3: Advanced Features (Priority: LOW)
- [ ] CVE timeline visualization
- [ ] Patch availability tracking
- [ ] Exploit maturity scoring
- [ ] Attack surface analysis
- [ ] Automated remediation recommendations

## Technical Documentation

### Reports Available

1. **БДУ ФСТЭК Integration Report** (`BDU_FSTEC_INTEGRATION_FINAL_REPORT.md`)
   - 30+ pages analysis
   - Three collector versions documented
   - Offline XLSX parser solution

2. **Affected Projects Enhancement** (`AFFECTED_PROJECTS_ENHANCEMENT_REPORT.md`)
   - 40+ pages technical details
   - 221 regex patterns documented
   - Before/after comparison: 2.6% → 78.1%

3. **Alternative CVE Sources** (`ALTERNATIVE_CVE_SOURCES_REPORT.md`)
   - 70+ pages comprehensive analysis
   - 10 sources evaluated
   - Implementation roadmap

4. **БДУ ФСТЭК Retry Report** (`BDU_FSTEC_RETRY_REPORT.md`)
   - 50+ pages detailed analysis
   - Site accessibility investigation
   - Manual download instructions

## Quick Start

### Prerequisites

```bash
pip install -r requirements_simple.txt
```

### View Statistics

```bash
python view_sqlite_database.py
```

### Query Database

```python
import sqlite3

conn = sqlite3.connect('data/cve_database.db')
c = conn.cursor()

# Your queries here
```

### Export to JSON

```bash
python export_database_to_json.py
```

Output in `exports/` directory.

## Data Updates

### Recommended Update Frequency

- **NVD**: Daily (new CVE published continuously)
- **GitHub Advisory**: Weekly
- **OSV**: Weekly
- **Intelligent Scoring**: After each data update

### Update Commands

```bash
# Full update
python collect_nvd_api.py
python collect_github_advisories.py
python collect_osv_vulnerabilities.py
python enhance_affected_projects.py
python intelligent_scoring_system.py

# Export updated data
python export_database_to_json.py
```

## License

This database aggregates publicly available CVE data from:
- NVD (NIST) - Public Domain
- GitHub Security Advisory - Community Data
- OSV - Open Source Vulnerabilities

The collection scripts and enhancements are provided as-is for security research and vulnerability management purposes.

## Credits

**Data Sources:**
- [NIST National Vulnerability Database](https://nvd.nist.gov/)
- [GitHub Security Advisory Database](https://github.com/advisories)
- [Open Source Vulnerabilities](https://osv.dev/)

**Related Projects:**
- Container News Digest System
- Release Monitoring System
- Telegram Security Bot

## Contact

For questions, issues, or contributions, please refer to the project repository.

---

**Database Version:** 1.0
**Export Date:** November 11, 2025
**Total CVE:** 343
**Last Collector Run:** NVD API v2.0 (333 CVE collected)
