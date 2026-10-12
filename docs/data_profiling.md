# Data Profiling Report

## Dataset

Train Service Passenger Counts FY2024-25

Source:
Victorian Department of Transport and Planning

Sample Size Analysed:
50,000 records

---

# Schema Summary

Total Columns: 21

## Categorical Fields

- Day_of_Week
- Day_Type
- Mode
- Train_Number
- Line_Name
- Group
- Direction
- Origin_Station
- Destination_Station
- Station_Name

## Numeric Fields

- Station_Latitude
- Station_Longitude
- Station_Chainage
- Stop_Sequence_Number
- Passenger_Boardings
- Passenger_Alightings
- Passenger_Arrival_Load
- Passenger_Departure_Load

## Date / Time Fields

- Business_Date
- Arrival_Time_Scheduled
- Departure_Time_Scheduled

---

# Business Observations

## Transport Modes

| Mode | Records |
|--------|--------:|
| Metro Trains | 46,178 |
| V/Line | 3,822 |

Observation:

The dataset is predominantly Metro Trains services (92.4%) with a smaller proportion of V/Line services.

---

## Service Direction

| Direction | Records |
|-----------|--------:|
| Down (D) | 25,973 |
| Up (U) | 24,027 |

Observation:

The sample exhibits a near-balanced distribution between Up and Down services.

---

## Day Types

| Day Type | Records |
|-----------|--------:|
| Normal Weekday | 28,621 |
| School Holiday | 12,440 |
| Saturday | 4,898 |
| Sunday | 4,041 |

Observation:

Normal weekday services account for the majority of activity and will likely drive overall passenger demand trends.

---

## Top Rail Lines by Record Volume

| Line | Records |
|--------|--------:|
| Frankston | 6,631 |
| Mernda | 4,802 |
| Pakenham | 3,911 |
| Hurstbridge | 3,710 |
| Craigieburn | 3,377 |
| Werribee | 3,147 |
| Lilydale | 3,136 |
| Sandringham | 2,772 |
| Glen Waverley | 2,677 |
| Belgrave | 2,599 |

Observation:

Frankston, Mernda and Pakenham appear frequently within the sample and are strong candidates for detailed trend analysis and forecasting.

---

# Candidate Business Use Cases

## Demand Analysis

- Passenger demand by line
- Passenger demand by station
- Passenger demand by service
- Passenger demand by day type

## Growth Analysis

- Line growth trends
- Station growth trends
- Service growth trends

## Capacity Planning

- High utilisation services
- High utilisation stations
- Network pressure points

## Forecasting

- Monthly passenger demand forecasts
- Line-level forecasts
- Station-level forecasts
- Capacity utilisation forecasts

---


# Dataset Scale Assessment

## Full Dataset Size

| Metric | Value |
|----------|----------|
| FY2024-25 Record Count | 15,937,507 |
| FY2024-25 File Size | ~2.7 GB |
| Historical Coverage | FY2018-19 to FY2024-25 |
| Total Raw Data Size | ~16 GB |
| Estimated Total Records | 95+ Million |

### Observation

The dataset exceeds the scale typically suited to spreadsheets and small-memory analytics workloads.

PySpark has been selected as the primary framework for ingestion, transformation and profiling activities.

Snowflake will be used as the analytical warehouse for reporting and forecasting workloads.

## Cardinality Assessment

| Entity | Count |
|----------|----------:|
| Total Records (FY2024-25) | 15,937,506 |
| Distinct Lines | 23 |
| Distinct Stations | 315 |
| Distinct Train Services | 5,878 |

### Observation

The dataset exhibits a classic dimensional modelling pattern with a high-volume fact table and relatively low-cardinality dimensions.

The Line, Station and Train Service dimensions remain comparatively small while the Fact table contains over 15.9 million records for FY2024-25.

This structure is well suited to a star schema design within Snowflake and supports efficient analytical processing.

---

# Dataset Grain

## Source Record Example

A single record can represent:

```text
Business_Date        = 2024-07-01
Train_Number         = 2327
Line_Name            = Alamein
Station_Name         = Camberwell
Stop_Sequence_Number = 1
Passenger_Boardings  = 10
Passenger_Alightings = 0
```

This represents a train service calling at a specific station on a particular business date.

## Business Grain

One record represents:

```text
Business Date
+
Train Service
+
Station Stop
```

Key Attributes:

```text
Business_Date
Train_Number
Station_Name
Stop_Sequence_Number
```

### Example

```text
01-Jul-2024
Train 2327
Camberwell Station
Stop Sequence 1
```

Represents a single stop event for a train service operating on a business date.

---

# Dimensions

## DIM_DATE

Fields:

- Business_Date
- Day_of_Week
- Day_Type

---

## DIM_LINE

Fields:

- Line_Name
- Group
- Mode

---

## DIM_STATION

Fields:

- Station_Name
- Station_Latitude
- Station_Longitude
- Station_Chainage

---

## DIM_DIRECTION

Fields:

- Direction

---

## DIM_TRAIN_SERVICE

Fields:

- Train_Number
- Origin_Station
- Destination_Station

---

# Fact Measures

The following measures will form the Fact table.

| Measure | Description |
|----------|-------------|
| Passenger_Boardings | Number of passengers boarding |
| Passenger_Alightings | Number of passengers alighting |
| Passenger_Arrival_Load | Passenger load arriving at station |
| Passenger_Departure_Load | Passenger load departing station |

## Derived Measures

The following metrics will be calculated in the Silver and Gold layers to support reporting, forecasting and planning analysis.

| Derived Measure | Business Definition |
|----------------|---------------------|
| Total Passenger Activity | Passenger_Boardings + Passenger_Alightings |
| Net Passenger Change | Passenger_Boardings - Passenger_Alightings |
| Average Passenger Load | Average Passenger_Departure_Load |
| Peak Passenger Load | Maximum Passenger_Departure_Load |
| Average Station Boardings | Average Passenger_Boardings by Station |
| Average Station Alightings | Average Passenger_Alightings by Station |
| Line Passenger Volume | Sum of Passenger_Boardings by Line |
| Station Passenger Volume | Sum of Passenger_Boardings by Station |
| Capacity Utilisation | Passenger_Departure_Load relative to network average |
| Month-over-Month Growth | Current Month Passenger Volume versus Previous Month |
| Year-over-Year Growth | Current Year Passenger Volume versus Previous Year |
| Passenger Share % | Passenger Volume as a proportion of total network demand |

---

## Fact Table Purpose

The Fact table captures passenger activity and train utilisation at the train service stop level.

The measures support:

- Passenger demand analysis
- Passenger movement analysis
- Service utilisation analysis
- Capacity planning
- Growth analysis
- Forecasting
- Planning and reporting

Example:

Business Date: 2024-07-01
Train Number: 2327
Station: Camberwell

Passenger_Boardings: 10
Passenger_Alightings: 0
Passenger_Arrival_Load: 0
Passenger_Departure_Load: 10

This allows passenger demand and train utilisation to be analysed at station, line, service and network levels.

---

# Analytical Opportunities

## Passenger Demand Analysis

Questions:

- Which lines are carrying the most passengers?
- Which stations are carrying the most passengers?
- How has demand changed over time?

---

## Growth Analysis

Questions:

- Which corridors are growing fastest?
- Which stations are growing fastest?

---

## Capacity Planning

Questions:

- Which services operate with the highest passenger loads?
- Which stations experience the highest utilisation?

---

## Forecasting

Questions:

- What passenger demand can be expected in FY2025-26?
- What passenger demand can be expected in FY2026-27?
- Which lines may experience future capacity pressures?

---

# Architecture Implications

Based on dataset size and structure:

## Ingestion

PySpark

## Storage

Parquet

## Data Warehouse

Snowflake

## Forecasting

Python + Prophet

## Reporting

Power BI

---

# Key Findings

# Data Quality Assessment

## Date Coverage

| Metric | Value |
|----------|----------|
| Minimum Date | 2024-07-01 |
| Maximum Date | 2025-06-30 |

Observation:

The dataset provides complete coverage for FY2024-25.

---

## Null Analysis

| Column | Null Count |
|----------|----------:|
| Arrival_Time_Scheduled | 14,591 |
| Departure_Time_Scheduled | 14,591 |

All remaining columns contain zero null values.

Observation:

The dataset exhibits a very high degree of completeness. Null values are limited to scheduled arrival and departure time fields and represent less than 0.1% of total records.

---

## Duplicate Analysis

| Metric | Value |
|----------|----------:|
| Duplicate Records | 0 |

Observation:

No duplicate records were identified using the business grain:

```text
Business_Date
Train_Number
Station_Name
Stop_Sequence_Number
```

This confirms that each train stop event is uniquely represented.

---

## Time Field Profiling

Observation:

PySpark inferred:

```text
Arrival_Time_Scheduled     → Timestamp

Departure_Time_Scheduled   → Timestamp
```

However, the source dataset contains time-only values.

During profiling, Spark automatically assigned a default date component when converting the values to timestamps.

For Bronze ingestion these fields will be retained as string values and converted to appropriate time data types during Silver transformations.

## Finding 1

The dataset contains over 15.9 million records for FY2024-25 and more than 16 GB of raw historical data across all financial years.

## Finding 2

The dataset provides station-level, service-level and line-level passenger activity, enabling detailed demand and capacity analysis.

## Finding 3

Passenger load metrics provide an opportunity to analyse service utilisation and future capacity pressure across the rail network.

## Finding 4

The dataset supports forecasting at multiple levels including network, line and station demand.

## Finding 5

The dataset is exceptionally complete with no null values identified across 19 of the 21 columns.

## Finding 6

No duplicate records were identified using the dataset business grain, indicating a high-quality source dataset suitable for analytical processing.

# Next Steps

1. Profile full dataset using PySpark
2. Create Bronze Layer
3. Build dimensional model
4. Create Silver Layer
5. Create analytical Gold Layer
6. Develop forecasting models
7. Build Power BI dashboards


---



# Current Status

✅ Dataset Downloaded

✅ Schema Discovered

✅ Dataset Grain Identified

✅ Data Dictionary Completed

✅ Solution Architecture Completed

✅ Data Model Designed

⏳ Full Dataset Profiling

⏳ Bronze Ingestion

⏳ Silver Transformations

⏳ Gold Layer Development

⏳ Forecasting

⏳ Power BI Dashboard Development


