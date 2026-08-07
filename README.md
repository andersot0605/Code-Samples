# Hi there, I'm Trevor Anderson 👋
**Senior Principal Systems Engineer | Infrastructure as Code Strategist | Enterprise Automation Architect**  
*Omaha, Nebraska | TSSCI

---

## 🚀 Executive Summary & Professional Mission

I am an enterprise systems engineer specializing in building high-velocity, zero-downtime infrastructure automation for highly regulated and secure computing environments. My core mission is to bridge the gap between complex cyber security demands and daily business operations. 

Over my career, I have designed and deployed full-stack automation frameworks that manage infrastructure from the physical datacenter hardware layer through virtualization, storage, and operating systems up to modern cloud and configuration management paradigms. I specialize in using Ansible as a universal automation glue layer—connecting disparate APIs, internal repositories, ticketing engines, and credential managers into single, cohesive business workflows.

---

## 🏆 Signature Professional Achievement: The VAMPR Framework

As the pinnacle of my technical portfolio, I architected, engineered, and deployed **VAMPR** (Vulnerability Analysis & Management of Patching and Remediation), a mature cyber threat mitigation engine built to safeguard enterprise Linux infrastructure.

### The Business Challenge
In modern enterprise environments, traditional patching cycles take anywhere from 14 to 30 days to implement, creating an unacceptable window of exposure. With the rise of AI-driven, automated attack tools and fast-moving exploits like **Mythos** and **Glasswing**, hostile actors can weaponize system vulnerabilities at unprecedented speeds. 

### The Solution & Business Impact
VAMPR compresses this multi-week security exposure down to a **strict sub-24-hour window**—completely shifting the organization from a reactive security posture to a proactive, automated defense system.
*   **Daily Zero-Touch Remediation:** Runs an automated pipeline every single day to query live vulnerability scan engines, resolve complex repository mappings, and deploy targeted software remediations.
*   **Zero Service Disruption:** Minimizes operational impact by using custom in-memory text filtering to automatically separate low-risk patches from high-impact upgrades (such as kernel, systemd, or glibc changes) that require service restarts, keeping critical business tools online.
*   **Zero Trust Architecture:** Operates with absolute credential volatility, utilizing temporary, single-use security tokens to securely authenticate API workflows across the network before safely scrubbing execution data from local systems.
*   **Real-Time SIEM Visibility:** Feeds granular telemetry data directly into central Splunk dashboards to give corporate leadership and compliance auditors an honest, live look at fleet-wide security compliance.

---

## 🛠️ Core Capabilities & Strategic Focus

*   **Ansible Mastery at Scale:** Expert-level creation of modular playbooks, dynamic inventories, custom collections, and highly performant API integrations leveraging native modules and direct REST abstractions.
*   **Red Hat Enterprise Linux Ecosystems:** Comprehensive architecture, management, and performance tuning across RHEL 6 through RHEL 9 ecosystems, including Red Hat Satellite, Identity Management (FreeIPA/IDM), and OS hardening.
*   **Infrastructure as Code (IaC):** Developing repeatable, stateful datacenter build workflows combining Terraform, Ansible, and Python script hooks to ensure business continuity and seamless disaster recovery models.
*   **Virtualization & Enterprise Storage:** Advanced operational oversight of high-throughput datacenter fabrics handling petabytes of data daily, built across VMware vSphere/VCF, Dell EMC storage arrays, and enterprise compute nodes.

---

## 📂 What You'll Find In This Repository

This repository serves as my public engineering portfolio, showcasing clean, dependency-free, and highly portable automation patterns engineered to run anywhere—including heavily restricted or air-gapped networks:

*   **VAMPR Subdirectory (`/VAMPR`):** The blueprint and core workflow orchestration configurations behind my daily automated sub-24-hour vulnerability patch pipeline.
*   **Enterprise Operational Playbooks:** Clean, open-source utilities built to handle master inventory aggregations, server registration health checks, and secure credential rotations.
*   **Storage-as-Code Utilities:** Automated storage management playbooks designed to query, map, and audit Network File System (NFS) environments across Dell EMC arrays and cross-reference them with active client hosts.

---

## 🤝 Let's Connect

I am always open to discussing advanced enterprise infrastructure design, large-scale RHEL environments, automated vulnerability remediation strategies, and configuration management within cleared, regulated spaces.

*   **LinkedIn:** [Trevor Anderson](https://linkedin.com)  
*   **GitHub Portfolio:** [andersot0605](https://github.com)
*   **Interests Beyond Engineering:** Outside of tech, I am always up for a conversation about golf, working out, bowling, video games, anime, or pop culture.

> *"Automate everything you think you'll do more than twice."*
