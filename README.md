# 🛡️☁️ AWS DevSecOps Pipeline: End-to-End Cloud Security

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9-blue)
![AWS](https://img.shields.io/badge/AWS-Fargate%20%7C%20WAF-orange)
![Security](https://img.shields.io/badge/Security-SAST%20%7C%20DAST%20%7C%20SCA-red)

## 📖 Executive Summary
This project demonstrates a secure, serverless 3-tier web application architecture on AWS. It implements a **"Shift Left"** methodology by integrating automated security gates (SAST, SCA) into the CI/CD workflow and a **"Shield Right"** strategy using active runtime protection (WAF) and intelligent threat detection (GuardDuty).

**Role:** Cloud Security Engineer / DevOps Engineer
**Tech Stack:** AWS (Fargate, ECS, ECR, ALB, WAF, GuardDuty), Docker, Python (Flask), GitHub Actions, Trivy, Bandit, OWASP ZAP.

---

## 🏗️ Architecture
The infrastructure is designed with strict network isolation, utilizing public subnets for the Load Balancer and private subnets for the application logic.

```text
+-----------------------------------------------------------------------------------+
|  AWS Cloud (VPC)                                                                  |
|                                                                                   |
|  +---------------------------+             +---------------------------+          |
|  |  Public Subnet            |             |  Private Subnet           |          |
|  |                           |             |                           |          |
|  |   [Internet Gateway]      |             |   [ECS Fargate Task]      |          |
|  |           |               |             |   +-------------------+   |          |
|  |           v               |             |   |  Flask App        |   |          |
|  |   [AWS WAF] (Security)    |             |   |  (Port 5000)      |   |          |
|  |           |               |             |   +---------^---------+   |          |
|  |           v               |             |             |             |          |
|  |   [Application LB] +------------------------------>   |             |          |
|  |   (Port 80 -> 5000)       |             |             |             |          |
|  +---------------------------+             +---------------------------+          |
|                                                                                   |
|  +-------------------------------------------------------------+                  |
|  |  Security Services                                          |                  |
|  |  [GuardDuty] ---> Monitors VPC Flow Logs & CloudTrail       |                  |
|  |  [ECR Registry] <--- Image Pull (Fargate)                   |                  |
|  +-------------------------------------------------------------+                  |
+-----------------------------------------------------------------------------------+

```

---

## 📂 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── build.yml      # CI/CD Pipeline (Trivy, Bandit, ZAP)
├── docs/                  # Screenshots and diagrams
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

> **Evidence:** See `docs/bandit-scan.jpg` for B104 binding detection.

### 2. Software Composition Analysis (SCA) - *Trivy*

Scans Docker container base images and Python dependencies for CVEs.

* **Policy:** Builds fail on "Critical" severity findings.
* **Remediation:** Automated checks ensure Flask and Werkzeug are patched against known vulnerabilities (e.g., CVE-2024-34069).

> **Evidence:** See `docs/trivy-failure.jpg` where the pipeline blocked a build due to High Severity CVEs.

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

### 1. Local Development

Clone the repo and run the container locally to verify functionality:

```bash
git clone [https://github.com/yourusername/aws-devsecops-project.git](https://github.com/yourusername/aws-devsecops-project.git)
docker build -t flask-app .
docker run -p 5000:5000 flask-app

```

### 2. Deployment to AWS (Manual Push)

The application is deployed to Amazon Elastic Container Registry (ECR) via the CLI.

**Step A: Authenticate with ECR**

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

```

**Step B: Build & Tag the Image**

```bash
docker build -t my-secure-app .
docker tag my-secure-app:latest <YOUR_AWS_ACCOUNT_ID>[.dkr.ecr.us-east-1.amazonaws.com/my-secure-app:latest](https://.dkr.ecr.us-east-1.amazonaws.com/my-secure-app:latest)

```

**Step C: Push to ECR**

```bash
docker push <YOUR_AWS_ACCOUNT_ID>[.dkr.ecr.us-east-1.amazonaws.com/my-secure-app:latest](https://.dkr.ecr.us-east-1.amazonaws.com/my-secure-app:latest)

```

*Once pushed, the ECS Fargate service is updated to pull the `latest` image tag.*

---

## ⚠️ Challenges & Resolutions (War Stories)

### 🔴 The "Firewall" Blocker

**Issue:** Load Balancer was unreachable; application timed out.
**Root Cause:** ALB was assigned the default Security Group blocking inbound traffic.
**Resolution:** Attached a custom SG allowing inbound HTTP from `0.0.0.0/0`.

### 🔴 502 Bad Gateway

**Issue:** Users received 502 errors despite healthy targets.
**Root Cause:** Port mismatch. ALB sent traffic to Port 80, but container listened on Port 5000.
**Resolution:** Reconfigured Target Group to map Port 80 -> 5000.

> **Evidence:** See `docs/502-error.jpg`.

### 🔴 ECR Pull Failures

**Issue:** Fargate tasks stuck in "PENDING".
**Root Cause:** Tasks in public subnets lacked Public IPs to reach ECR.
**Resolution:** Enabled "Auto-assign Public IP".

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
