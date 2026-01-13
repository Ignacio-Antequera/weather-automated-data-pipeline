{{ config(
    materialized='table',
    schema='mart'
) }}

SELECT
    city,
    temperature,
    weather_description,
    wind_speed,
    weather_time_local
FROM {{ ref('stg_weather_data') }}