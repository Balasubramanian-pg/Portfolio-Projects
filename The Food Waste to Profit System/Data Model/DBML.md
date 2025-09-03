# DBML Schema for Food Waste Reduction Dashboard

```dbml
Table dim_date {
  date_id date [pk]
  date date
  day_of_week varchar
  day_of_week_number integer
  is_weekend boolean
  month_name varchar
  month_number integer
  quarter varchar
  year integer
}

Table dim_restaurant {
  restaurant_id integer [pk]
  restaurant_name varchar
  restaurant_code varchar
  manager_name varchar
  city varchar
  region varchar
  is_pilot_location boolean
}

Table dim_waste_item {
  waste_item_id integer [pk]
  waste_item_name varchar
  category varchar
  standard_cost decimal
}

Table dim_waste_reason {
  waste_reason_id integer [pk]
  waste_reason varchar
}

Table dim_partner {
  partner_id integer [pk]
  partner_name varchar
  partner_type varchar
  contact_info varchar
}

Table fact_waste_log {
  waste_log_id bigint [pk]
  date_id date [ref: > dim_date.date_id]
  restaurant_id integer [ref: > dim_restaurant.restaurant_id]
  waste_item_id integer [ref: > dim_waste_item.waste_item_id]
  waste_reason_id integer [ref: > dim_waste_reason.waste_reason_id]
  quantity decimal
  unit_of_measure varchar
  estimated_cost decimal
}

Table fact_redistribution {
  redistribution_id bigint [pk]
  date_id date [ref: > dim_date.date_id]
  restaurant_id integer [ref: > dim_restaurant.restaurant_id]
  partner_id integer [ref: > dim_partner.partner_id]
  waste_item_id integer [ref: > dim_waste_item.waste_item_id]
  quantity_diverted decimal
  unit_of_measure varchar
  disposal_cost_savings decimal
  potential_revenue decimal
}
```

This DBML (Database Markup Language) schema defines the structure needed for the food waste reduction dashboard. It includes:

1. **Dimension Tables** that describe the key entities:
   - `dim_date` for time-based analysis
   - `dim_restaurant` for location information
   - `dim_waste_item` for categorizing wasted food items
   - `dim_waste_reason` for tracking why waste occurred
   - `dim_partner` for tracking redistribution channels

2. **Fact Tables** that store the measurable events:
   - `fact_waste_log` for recording each waste occurrence
   - `fact_redistribution` for tracking successful waste diversion

The relationships between tables are defined using foreign key references, creating a star schema that's optimized for analytical queries in Power BI. This structure will allow for comprehensive reporting on waste reduction efforts, cost savings, and the impact of redistribution programs.

<img width="1404" height="776" alt="Untitled" src="https://github.com/user-attachments/assets/95e43ad0-fc72-4fe5-b1c2-be7798e21ae8" />
