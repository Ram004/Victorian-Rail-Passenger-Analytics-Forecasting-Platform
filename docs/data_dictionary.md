# Data Dictionary

## Dataset

**Source*** Victorian Department of Transport and Planning Open Data

**Dataset:** Train Service Passenger Counts

**Description:**
The dataset provides estimated passenger boardings, alightings and service loads for train services operating across the Victorian rail network. Each record represents a train service stop at a station for a given business date.

---

## Dataset Grain

One record represents:

```text
Business Date
+
Train Service
+
Station Stop
```

This allows analysis at:

- Network Level
- Line Level
- Train Service Level
- Station Level
- Time Level

---

## Column Definitions

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| Business_Date | Date | Business service date used for reporting and analytics. |
| Day_of_Week | String | Day name corresponding to the business date. |
| Day_Type | String | Classification of the day (e.g. Weekday, Weekend, School Holiday, Public Holiday). |
| Mode | String | Transport operator category, typically Metro Trains or V/Line. |
| Train_Number | String | Unique train service identifier. |
| Line_Name | String | Name of the train line on which the service operates. |
| Group | String | Rail corridor grouping used by the transport network. |
| Direction | String | Train direction. U = Up (towards Flinders Street), D = Down (away from Flinders Street). |
| Origin_Station | String | First station for the train service. |
| Destination_Station | String | Final station for the train service. |
| Station_Name | String | Station associated with the stop record. |
| Station_Latitude | Decimal | Latitude coordinate of the station. |
| Station_Longitude | Decimal | Longitude coordinate of the station. |
| Station_Chainage | Integer | Distance reference used by rail infrastructure systems. |
| Stop_Sequence_Number | Integer | Order of the stop within the train service. |
| Arrival_Time_Scheduled | Time | Scheduled arrival time of the train service at the station. |
| Departure_Time_Scheduled | Time | Scheduled departure time of the train service from the station. |
| Passenger_Boardings | Integer | Estimated number of passengers boarding at the station. |
| Passenger_Alightings | Integer | Estimated number of passengers alighting at the station. |
| Passenger_Arrival_Load | Integer | Estimated passenger load on the train upon arrival at the station. |
| Passenger_Departure_Load | Integer | Estimated passenger load on the train after departure from the station. |

---

## Measures

The following columns will be treated as analytical measures:

| Measure | Description |
|----------|-------------|
| Passenger_Boardings | Number of passengers boarding the service. |
| Passenger_Alightings | Number of passengers alighting from the service. |
| Passenger_Arrival_Load | Passenger load arriving at the station. |
| Passenger_Departure_Load | Passenger load departing the station. |

---

## Candidate Dimensions

### Date Dimension

Fields:

- Business_Date
- Day_of_Week
- Day_Type

Purpose:

Supports trend analysis and forecasting.

---

### Line Dimension

Fields:

- Line_Name
- Group
- Mode

Purpose:

Supports line-level reporting and growth analysis.

---

### Train Service Dimension

Fields:

- Train_Number
- Origin_Station
- Destination_Station

Purpose:

Supports service-level utilisation analysis.

---

### Station Dimension

Fields:

- Station_Name
- Station_Latitude
- Station_Longitude
- Station_Chainage

Purpose:

Supports station-level analytics and geospatial reporting.

---

### Direction Dimension

Fields:

- Direction

Purpose:

Supports directional demand analysis.

---

## Analytical Use Cases

The dataset supports:

### Demand Analysis

- Total passenger demand
- Passenger demand by line
- Passenger demand by station
- Passenger demand by service

### Growth Analysis

- Year-over-Year growth
- Station growth trends
- Line growth trends

### Capacity Analysis

- High utilisation services
- High utilisation stations
- Capacity pressure identification

### Forecasting

- Future passenger demand
- Future line growth
- Future station demand
- Capacity planning scenarios

### Planning and Decision Support

- Network planning
- Service planning
- Capacity assessments
- Growth corridor identification