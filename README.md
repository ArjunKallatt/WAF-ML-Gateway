# 🛡️ WAF-ML Gateway: Intelligent Web Application Firewall

![Accuracy](https://img.shields.io/badge/Model_Accuracy-98.97%25-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-lightgrey)

## 📌 Overview
Traditional Web Application Firewalls (WAFs) rely heavily on static regular expressions, which are prone to bypasses and false positives. **WAF-ML Gateway** is a dynamic, intelligent security proxy that uses a **Random Forest Machine Learning model** to evaluate web traffic in real-time. 

By analyzing the lexical features and entropy of incoming URLs, it actively distinguishes between safe browsing traffic and malicious payloads (such as SQLi, XSS, and Path Traversal), forwarding clean traffic to its intended destination while instantly dropping threats.

## ✨ Key Features
* **High-Fidelity Threat Detection:** Achieved **98.97% accuracy** with an optimized Random Forest Classifier.
* **Massive Training Scale:** Trained on a comprehensive dataset of over **1.3 million** structured web requests.
* **Custom Feature Engineering:** Replaces traditional RegEx by mathematically evaluating requests using:
  * Shannon Entropy Analysis (detects obfuscated/encoded payloads)
  * Character & Keyword Distribution metrics
  * URL Length anomalies
* **Universal Dynamic Proxy:** Safely intercepts and resolves URLs, acting as a secure gateway for the host operating system.
* **Interactive Dashboard:** Features a clean, dark-themed UI to securely search and route traffic directly from `localhost`.

## 🧠 Architecture
The project is split into two core phases:
1. **The Brain (Model Training):** Raw HTTP requests are pre-processed to extract key numerical features. A Random Forest model is trained to minimize false positives while maintaining a high recall rate against zero-day syntax structures.
2. **The Shield (Flask Gateway):** A lightweight proxy intercepts local traffic, extracts features in milliseconds, and queries the `.pkl` model. Safe requests trigger an OS-level browser launch to the destination, while malicious requests are halted with a `403 Forbidden` response.

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* A Linux environment (Arch/Ubuntu) is recommended for optimal OS-level browser routing.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/ArjunKallatt/WAF-ML-Gateway.git](https://github.com/ArjunKallatt/WAF-ML-Gateway.git)
   cd WAF-ML-Gateway
