# Shift-Left Container Security with Trivy

[![Trivy Image Scan](https://img.shields.io/badge/Security-Trivy%20Integrated-46a2f1?style=for-the-badge&logo=aquasecurity)](https://github.com/hazzikri/trivy-container-security/actions)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions)](https://github.com/hazzikri/trivy-container-security/actions)
[![Docker](https://img.shields.io/badge/Target-Docker%20Image-2496ED?style=for-the-badge&logo=docker)](https://hub.docker.com/)
[![SARIF Upload](https://img.shields.io/badge/Reports-GitHub%20Security%20Tab-darkgreen?style=for-the-badge&logo=github)](https://docs.github.com/en/code-security)

A **Shift-Left DevSecOps** implementation that integrates **Trivy** (by Aqua Security) directly into the CI/CD pipeline to automatically detect container image vulnerabilities and infrastructure misconfigurations **before** code reaches production.

---

## 🔐 What This Project Demonstrates

This is a practical implementation of the same container security methodology applied in production at **PT Link Net Tbk**, where Trivy was embedded into Azure DevOps pipelines and configured to automatically break the build on CRITICAL vulnerabilities.

```
┌──────────────────────────────────────────────────────────────┐
│                   GitHub Actions Pipeline                    │
│                                                              │
│  ┌────────────┐   ┌─────────────────┐   ┌────────────────┐  │
│  │ Code Push  │──▶│  Docker Build   │──▶│  Trivy Image   │  │
│  │  to main   │   │  (Dockerfile)   │   │     Scan       │  │
│  └────────────┘   └─────────────────┘   └───────┬────────┘  │
│                                                  │           │
│                   ┌──────────────────────────────┘           │
│                   ▼                                          │
│          ┌─────────────────────┐   ┌─────────────────────┐  │
│          │  CRITICAL/HIGH CVE? │   │ GitHub Security Tab │  │
│          │   ──────────────    │──▶│   SARIF Report      │  │
│          │   YES → FAIL BUILD  │   │   (all severities)  │  │
│          │   NO  → PASS        │   └─────────────────────┘  │
│          └─────────────────────┘                            │
└──────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Pipeline Jobs

### Job 1: `trivy-image-scan`
Builds the Docker image from source, then scans it with Trivy:
- **Fails the build** if any `CRITICAL` or `HIGH` severity CVEs are found in OS packages or libraries.
- Generates a **SARIF report** uploaded to the GitHub Security tab for full audit trail.
- Ignores vulnerabilities with no available fix (`ignore-unfixed: true`) to avoid noise.

### Job 2: `trivy-config-scan`
Scans all IaC configuration files (Kubernetes YAML, Terraform HCL, Dockerfiles) in the repo:
- Detects security misconfigurations like running containers as root, exposed sensitive ports, or missing resource limits.
- Results appear in the GitHub Security tab for developer review.

---

## 🚀 Running Trivy Locally

### Scan a Docker Image
```bash
# Install Trivy (Linux)
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Scan an image from Docker Hub
trivy image python:3.12-slim

# Scan only CRITICAL and HIGH, fail if any found
trivy image --exit-code 1 --severity CRITICAL,HIGH python:3.12-slim
```

### Scan Local Filesystem / Config Files
```bash
# Scan current directory for misconfigurations
trivy config .

# Scan Kubernetes manifests
trivy config ./kubernetes/
```

### Build and Scan This Repo's App
```bash
docker build -t demo-app:local -f app/Dockerfile app/
trivy image --severity CRITICAL,HIGH demo-app:local
```

---

## 🔧 Key Configuration Decisions

| Decision | Reason |
|---|---|
| `exit-code: 1` on CRITICAL/HIGH | **Hard gate** — build cannot proceed if container has known exploitable CVEs |
| `ignore-unfixed: true` | Only flags issues with an available patch, reducing false positive noise |
| SARIF upload | Integrates into GitHub Advanced Security for centralized vulnerability management |
| Weekly scheduled scan | Catches newly-published CVEs in already-deployed images (runtime drift) |
| Config scan as non-blocking (`exit-code: 0`) | Misconfiguration findings go to Security tab as warnings, not build failures |

---

## 📌 Production Context

In the enterprise environment at PT Link Net Tbk, this pattern was extended with:
- **Azure DevOps integration** using the Trivy Azure Pipelines task.
- **Microsoft Defender for DevOps** for additional secret scanning and code security posture.
- **Automated Jira ticket creation** for any CRITICAL finding that required tracking across teams.
