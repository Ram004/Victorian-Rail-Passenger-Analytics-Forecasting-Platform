# Data Model

## Overview

The solution adopts a dimensional modelling approach to support analytical reporting, forecasting and capacity planning.

The model is designed around a central fact table containing passenger activity metrics and a collection of conformed dimensions that provide reporting context.

The model supports analysis at:

- Network Level
- Line Level
- Station Level
- Train Service Level
- Day Type Level
- Time Level

---

# Dataset Grain

The grain of the source dataset is:

```text
Business Date
+
Train Service
+
Station Stop
```

Business Keys:

```text
Business_Date
Train_Number
Station_Name
Stop_Sequence_Number
```

Each row represents a train service calling at a specific station on a specific business date.

---

# Star Schema

```text
                 DIM_DATE
                     |
                     |
DIM_LINE ---- FACT_PASSENGER_COUNTS ---- DIM_STATION
                     |
                     |
             DIM_DIRECTION
                     |
                     |
            DIM_TRAIN_SERVICE
```

---

# Fact Table

## FACT_PASSENGER_COUNTS

### Purpose

Stores passenger demand and service utilisation metrics.

### Grain

One train service stop at one station on one business date.

### Foreign Keys

| Column |
|----------|
| Date_Key |
| Line_Key |
| Station_Key |
| Direction_Key |
| Train_Service_Key |

### Measures

| Column | Description |
|----------|-------------|
| Passenger_Boardings | Number of passengers boarding |
| Passenger_Alightings | Number of passengers alighting |
| Passenger_Arrival_Load | Passenger load arriving at station |
| Passenger_Departure_Load | Passenger load departing station |

### Derived Measures

| Metric |
|-----------|
| Total Passengers |
| Load Change |
| Average Load |
| Peak Load |
| Growth Rate |
| Capacity Utilisation |

---

# Dimension Tables

## DIM_DATE

### Purpose

Provide time-based reporting and forecasting.

### Attributes

| Column |
|----------|
| Date_Key |
| Business_Date |
| Day_Of_Week |
| Day_Type |
| Month |
| Quarter |
| Year |
| Financial_Year |

### Example Use Cases

- Passenger demand by financial year
- Demand by weekday
- School holiday analysis
- Seasonal forecasting

---

## DIM_LINE

### Purpose

Support rail line reporting and trend analysis.

### Attributes

| Column |
|----------|
| Line_Key |
| Line_Name |
| Group |
| Mode |

### Example Use Cases

- Line growth analysis
- Passenger demand by corridor
- Line forecasting

---

## DIM_STATION

### Purpose

Support station-level analytics and geospatial reporting.

### Attributes

| Column |
|----------|
| Station_Key |
| Station_Name |
| Station_Latitude |
| Station_Longitude |
| Station_Chainage |

### Example Use Cases

- Station demand ranking
- Station growth analysis
- Mapping and geospatial visualisation

---

## DIM_DIRECTION

### Purpose

Support directional service analysis.

### Attributes

| Column |
|----------|
| Direction_Key |
| Direction |

### Values

```text
U = Up

D = Down
```

### Example Use Cases

- Directional passenger flows
- Morning and evening travel patterns

---

## DIM_TRAIN_SERVICE

### Purpose

Support train service utilisation analysis.

### Attributes

| Column |
|----------|
| Train_Service_Key |
| Train_Number |
| Origin_Station |
| Destination_Station |

### Example Use Cases

- Service utilisation
- Capacity analysis
- Passenger load analysis

---

# Gold Data Products

The following analytical datasets will be produced.

---

## GOLD_PASSENGER_DEMAND

### Purpose

Analyse historical demand trends.

### Grain

```text
Financial year
Month
Line
```

### Measures

- Total Boardings
- Total Alightings
- Total Passenger Activity (boardings + alightings)

---

## GOLD_LINE_GROWTH

### Purpose

Compare passenger demand by line and financial year.

### Measures

- Total boardings
- Total alightings

---

## GOLD_STATION_DEMAND

### Purpose

Analyse station boardings and alightings by month.

### Measures

- Boardings
- Alightings

---

## SERVICE_UTILISATION_ANALYSIS (planned, not implemented)

### Purpose

Assess service demand and utilisation.

### Measures

- Passenger Arrival Load
- Passenger Departure Load
- Maximum Service Load

---

## GOLD_CAPACITY_UTILISATION

### Purpose

Summarise passenger load by line to support capacity analysis.

### Measures

- Average arrival load and average departure load
- Peak departure load

---

## GOLD_FORECAST_INPUT

### Purpose

Provide the monthly boardings series used for forecasting and validation.

### Grain

```text
Month
Line
```

### Measures

- Passenger Boardings
- Passenger Alightings

---

# Forecasting Outputs

## NETWORK_DEMAND_FORECAST (planned, not implemented)

Forecast:

```text
Total Passenger Demand
```

---

## LINE_DEMAND_FORECAST (planned, not implemented)

Forecast:

```text
Passenger Demand By Line
```

Examples:

- Frankston
- Pakenham
- Mernda
- Craigieburn

---

## CAPACITY_FORECAST (planned, not implemented)

Forecast:

```text
Passenger_Arrival_Load

Passenger_Departure_