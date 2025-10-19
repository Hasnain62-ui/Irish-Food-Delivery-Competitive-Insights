# Business Intelligence Final Project: Irish Food Delivery Competitive Insights

## Project Overview

This project is the final deliverable for the MSc Entrepreneurship, Business Intelligence Module (H9BI).

The project employs data analytics to perform a **Competitive Intelligence** analysis on the leading food delivery platforms in Ireland: **Deliveroo, Just Eat, and Uber Eats**. The goal is to extract **actionable insights** for aspiring entrepreneurs or investors, validating the market landscape and identifying competitive advantages.

The core business question addressed is:
> **“Which platform demonstrates stronger customer satisfaction and operational performance, based on publicly available data, and what factors contribute to its competitive advantage?”**

***

## Final Artifact

### 1. Live Dashboard

The primary deliverable is an interactive, web-based Business Intelligence dashboard.

- **Live URL:** `https://hasnain62-ui.github.io/Irish-Food-Delivery-Competitive-Insights/`
- **Key Metrics:** Comparative customer ratings, sentiment analysis (polarity), and trends across platforms.

### 2. Submission Files

This repository contains all the code and documentation used to generate the dashboard.

| File/Folder | Description |
| :--- | :--- |
| `index.html` & `styles.css` | The static site files for the live dashboard presentation. |
| `competitive_insights_dashboard.ipynb` | The main Jupyter Notebook detailing all data cleaning, analytical steps, and visualization generation. |
| `scraper_*.py` | Python scripts used for initial data acquisition from public sources. |
| `data/` | Contains the raw and processed CSV files used for the analysis (e.g., Trustpilot and Google Play Store reviews). |
| `images/` | Contains static visualizations generated from the analysis notebook, embedded into the `index.html`. |
| `requirements.txt` | Lists all necessary Python packages for environment setup and reproducibility. |

***

## Setup and Reproducibility

To reproduce the analysis and environment, please follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/Hasnain62-ui/Irish-Food-Delivery-Competitive-Insights.git
cd Irish-Food-Delivery-Competitive-Insights
