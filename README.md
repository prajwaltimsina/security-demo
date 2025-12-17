# 🛡️☁️ AWS DevSecOps Pipeline: End-to-End Cloud Security

## 📖 Executive Summary

This project demonstrates a secure, serverless 3-tier web application architecture on AWS. It implements a **"Shift Left"** methodology by integrating automated security gates (SAST, SCA) into the CI/CD workflow and a **"Shield Right"** strategy using active runtime protection (WAF) and intelligent threat detection (GuardDuty).

**Role:** Cloud Security Engineer / DevOps Engineer
**Tech Stack:** AWS (Fargate, ECS, ECR, ALB, WAF, GuardDuty), Docker, Python (Flask), GitHub Actions, Trivy, Bandit, OWASP ZAP.

---

## 🏗️ Architecture

The infrastructure is deployed using Terraform/CloudFormation with a focus on strict network isolation.

```mermaid
graph TD
    subgraph "AWS Cloud (VPC)"
        subgraph "Public Subnet"
            IGW[Internet Gateway]
            ALB[Application Load Balancer]
            WAF["AWS WAF - ACL Rules"]
        end
        
        subgraph "Private Subnet"
            Fargate[ECS Fargate Task]
            App[Python Flask App]
        end
        
        subgraph "Security Services"
            GD["GuardDuty (Threat Detection)"]
            ECR["ECR (Image Registry)"]
        end
    end

    User((User)) -->|HTTPS Traffic| WAF
    WAF -->|Filtered Traffic| ALB
    ALB -->|Port 80 -> 5000| Fargate
    Fargate --> App
    Fargate -.->|Pull Image| ECR

---

---

## 📂 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml      # CI/CD Pipeline (Trivy, Bandit, ZAP, Build & Push)
├── app.py                 # Vulnerable Python Flask application (The Target)
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies (Flask, Werkzeug, etc.)
├── bandit-scan.txt        # Output log from Static Analysis (SAST)
└── README.md              # Project documentation

```

---

## 🔐 Security Implementation

### 1. Static Analysis (SAST) - *Bandit*

Integrated into GitHub Actions to scan Python source code for insecure logic (e.g., hardcoded bindings, shell injection risks) before the build stage.

### 2. Software Composition Analysis (SCA) - *Trivy*

Scans Docker container base images and Python dependencies for CVEs.

* **Policy:** Builds fail on "Critical" severity findings.
* **Remediation:** Automated checks ensure Flask and Werkzeug are patched against known vulnerabilities (e.g., CVE-2024-34069).

### 3. Dynamic Analysis (DAST) - *OWASP ZAP*

Automated baseline scan against the staging environment to identify runtime vulnerabilities.

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://<LOAD_BALANCER_DNS>/

```

### 4. Runtime Protection - *AWS WAF & GuardDuty*

* **WAF:** Deployed with Managed Rule Groups (Core Rule Set, Linux OS) to block SQLi, XSS, and LFI attacks.
* **GuardDuty:** Monitors CloudTrail and VPC Flow Logs for anomalous behavior.

---

## 🛠️ Installation & Usage

### Prerequisites

* AWS CLI configured with Administrator access
* Docker Desktop installed
* Terraform installed

### Local Development

1. Clone the repo:
```bash
git clone https://github.com/yourusername/aws-devsecops-project.git

```


2. Build the container:
```bash
docker build -t flask-app .

```


3. Run locally:
```bash
docker run -p 5000:5000 flask-app

```



### Deployment

To deploy the infrastructure to AWS:

```bash
cd terraform/
terraform init
terraform apply

```

---

## ⚠️ Challenges & Resolutions (War Stories)

* **The "Firewall" Blocker:** Resolved ALB timeouts by replacing the default Security Group with a custom SG allowing inbound HTTP from 0.0.0.0/0.
* **502 Bad Gateway:** Fixed port mismatch between ALB (Port 80) and Container (Port 5000) by reconfiguring the Target Group.
* **ECR Pull Failures:** Enabled "Auto-assign Public IP" for Fargate tasks in public subnets to allow image pulling.

---

