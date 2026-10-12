# Metro Rail Passenger Demand Forecasting & Capacity Planning Platform

## Overview

An end-to-end analytics solution designed to analyse Victorian rail passenger demand, identify long-term trends, forecast future patronage, and support network planning decisions.

The project leverages seven financial years of Victorian train service passenger count data to understand passenger behaviour, assess post-COVID recovery patterns, identify growth corridors, forecast future demand, and evaluate potential capacity pressures across the rail network.

This project demonstrates a complete Data Analyst workflow including data ingestion, data quality assessment, dimensional modelling, business analytics, forecasting, dashboarding, and stakeholder-focused recommendations.

---

## Business Problem

Metro's Performance, Planning and Reporting teams rely on data-driven insights to support operational planning and decision-making.

This project seeks to answer the following questions:

### Demand Analysis

- How has passenger demand changed between FY2018-19 and FY2024-25?
- What impact did COVID-19 have on passenger patronage?
- How has passenger demand recovered following the pandemic?

### Network Growth

- Which rail lines are experiencing the strongest growth?
- Which stations show the highest increases in passenger activity?
- Which services have experienced the largest changes in demand?

### Capacity Planning

- Which parts of the network are experiencing increasing utilisation?
- Which services may face future capacity constraints?
- Which routes should be prioritised for monitoring and planning?

### Forecasting

- What passenger demand can be expected during FY2025-26 and FY2026-27?
- How might future growth impact network performance and capacity?

---

## Dataset

Source:

Victorian Department of Transport and Planning Open Data

Dataset:

Train Service Passenger Counts

Coverage:

- FY2018-19
- FY2019-20
- FY2020-21
- FY2021-22
- FY2022-23
- FY2023-24
- FY2024-25

The dataset contains train service-level passenger boardings, alightings and passenger load information across the Victorian metropolitan and regional rail network.

---

## Solution Architecture

```text
Victorian Open Transport Data
         |
         v

Landing Zone (CSV Files)
         |
         v

Bronze Layer (PySpark)
Raw Historical Data
Schema Discovery
Data Profiling
Parquet Conversion
         |
         v

Silver Layer
Data Quality Validation
Data Cleansing
Dimensional Modelling
         |
         v

Snowflake Analytics Warehouse
         |
         v

Gold Layer
Business Data Products
Growth Analysis
Capacity Analysis
Forecast Inputs
         |
         v

Python Forecasting Engine
Prophet
Moving Average Models
         |
         v

Forecast Results
         |
         v

Power BI Dashboards
         |
         v

Business Recommendations
```

---

## Medallion Architecture

### Bronze Layer

Purpose:

Preserve raw historical datasets and establish the foundation for analytics.

Activities:

- CSV ingestion
- Schema discovery
- Data profiling
- Metadata capture
- Conversion to Parquet

Outputs:

- bronze_passenger_counts

---

### Silver Layer

Purpose:

Create clean, validated and business-ready datasets.

Activities:

- Data quality assessment
- Null handling
- Data type standardisation
- Business rule validation
- Dimensional modelling

Fact Tables:

- fact_passenger_counts

Dimension Tables:

- dim_date
- dim_line
- dim_direction

---

### Gold Layer

Purpose:

Deliver business-focused analytical datasets for reporting and forecasting.

Business Views:

- passenger_demand_summary
- line_growth_analysis
- station_growth_analysis
- capacity_risk_analysis
- network_performance_summary
- forecast_input

---

## Data Quality Framework

The project incorporates data quality validation prior to business reporting.

Checks include:

- Missing values
- Duplicate records
- Invalid dates
- Invalid passenger counts
- Data completeness
- Data consistency

Outputs:

- Data quality scorecards
- Exception reporting
- Data profiling summaries

---

## Forecasting Approach

The project uses historical passenger demand patterns to estimate future network utilisation.

### Forecast Models

#### Baseline Forecast

- Moving Average Forecasting

#### Advanced Forecast

- Prophet Time-Series Forecasting

### Forecast Horizons

- FY2025-26
- FY2026-27

### Forecast Outputs

- Network Passenger Demand
- Line-Level Passenger Demand
- Capacity Utilisation Trends

---

## Scenario Planning

Scenario modelling is used to support operational planning decisions.

Scenarios:

### Current Demand

Baseline forecast.

### Moderate Growth

+10% passenger growth.

### High Growth

+20% passenger growth.

### Aggressive Growth

+30% passenger growth.

Business Questions:

- Which lines may require additional services?
- Which stations may experience future demand pressure?
- Which corridors should be prioritised for planning activities?

---

## Power BI Dashboards

### Executive Overview

- Total Passenger Demand
- Year-on-Year Growth
- Forecast Passenger Demand
- High Growth Corridors

### Passenger Demand Analysis

- Historical Demand Trends
- COVID Impact Analysis
- Recovery Patterns

### Growth Analysis

- Fastest Growing Lines
- Fastest Growing Stations
- Growth Rankings

### Capacity Planning

- Capacity Risk Assessment
- Service Utilisation Analysis
- Network Pressure Points

### Forecasting

- Passenger Demand Forecasts
- Confidence Intervals
- Scenario Modelling

### Data Quality

- Completeness Metrics
- Data Quality Exceptions
- Validation Results

---

## Technology Stack

### Data Engineering

- PySpark
- Parquet
- Medallion Architecture

### Data Warehouse

- Snowflake

### Analytics

- SQL
- Python
- Pandas (profiling and exploratory analysis)

### Forecasting

- Prophet
- Time-Series Analysis

### Reporting

- Power BI

### Source Control

- GitHub

---

## Project Structure

```text
metro-rail-demand-forecasting

├── README.md

├── data
│   ├── raw
│   ├── bronze
│   ├── silver
│   └── gold

├── docs
│   ├── architecture.md
│   ├── business_problem.md
│   ├── data_dictionary.md
│   ├── data_model.md
│   └── data_profiling.md

├── notebooks
│   ├── 01_bronze_ingestion.ipynb
│   ├── 02_data_profiling.ipynb
│   ├── 03_silver_transformation.ipynb
│   ├── 04_gold_analytics.ipynb
│   └── 05_forecasting.ipynb

├── sql
│   ├── create_tables.sql
│   ├── transformations.sql
│   └── analytics.sql

├── powerbi

├── screenshots

└── requirements.txt
```

---

## Key Outcomes

This project demonstrates:

- End-to-End Data Analytics
- Data Quality Management
- Data Modelling
- SQL Analytics
- Trend Analysis
- Forecasting & Modelling
- Capacity Planning
- Snowflake Analytics
- Python Analytics
- Power BI Development
- Data Storytelling
- Business Recommendations
- Decision Support

---

## Future Enhancements

- Weather correlation analysis
- Public holiday impact modelling
- Station-level forecasting
- Service-level forecasting
- Reliability and punctuality integration
- Real-time network monitoring
- Passenger demand anomaly detection