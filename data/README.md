# Stanford Transportation - ChargePoint EV Chargers Dashboard Data - 2023

This dataset is a collection of data tables downloaded from Stanford University's ChargePoint EV charger dashboard
between Sep-2023 and Dec-2023.

The tables are provided as-is, oddities and all. Refer to the following section for some guidelines on how to clean the
data.

## Data Cleaning Guidelines

### Charging Sessions

The charging session tables (located in `reports\analytics`) contain the following oddities that should be corrected
before normative processing:

- `System S/N` column is represented in scientific notation and should be converted to an integer string