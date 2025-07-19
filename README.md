# 🧠 Medical Equipment Utilization & Fault Diagnosis System | GenAI-Powered

> **Leverage Generative AI to automate medical equipment monitoring, safety compliance, and smart technician interaction.**

---

## 🚀 Overview

This intelligent system streamlines hospital equipment diagnostics using **GPT-4o**, transforming unstructured brochure data and live operational logs into actionable insights. It extracts specifications from equipment manuals (PDF), analyzes real-time usage data (CSV), flags threshold violations, summarizes risks, and even enables natural-language interaction for technicians/admins.

---

## 🎯 Key Capabilities

- 🧾 **Brochure Parsing**  
  Extracts technical specifications (e.g., temperature limits, pressure thresholds, calibration intervals) from equipment PDFs.

- 📊 **Live Usage Data Analysis**  
  Monitors equipment performance in real time using CSV logs.

- ⚠️ **Violation Detection**  
  Detects abnormal readings and generates violation reports based on brochure-defined limits.

- 📋 **Automated Risk Summarization**  
  Summarizes potential risks in plain language for hospital staff.

- 💬 **Chat Agent for Admins/Technicians**  
  Ask domain-specific questions like:
  - *“Which device exceeded temperature limits?”*
  - *“Is any equipment overdue for calibration?”*

- 🧠 **Powered by OpenAI GPT Models**  
  Model configurable via `config/config.yaml` using providers like OpenAI.

---

## 🏗️ Project Architecture

```bash
📦 Medical-Equipment-Utilization-Fault-Diagnosis-System
├── agents/
│   ├── specs_agent.py         # Parses brochure and extracts limits
│   ├── violation_agent.py     # Flags safety violations
│   ├── summary_agent.py       # Summarizes safety risks
│   └── chat_agent.py          # Answers technician/admin queries
│
├── config/
│   └── config.yaml            # Model and API configuration
│
├── data/
│   └── live_equipment_data.csv # Sample live usage logs
│
├── docs/
│   └── MRI_brochure.pdf       # Sample equipment brochure
│
├── results/
│   └── final_diagnosis.txt    # Workflow outputs
│
├── utils/
│   └── model_loader.py        # Loads & validates LLM config
│
├── main.py                    # Entry point for the workflow
├── test_gpt.py                # Test script to check GPT response
└── README.md                  # Project documentation
