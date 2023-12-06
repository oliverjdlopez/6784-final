# Weather
This plugin collects all the weather data related to the Cineca facility location (Casalecchio di Reno) using an online open weather service  (https://openweathermap.org). 

NOTE: In ExaMon forecasts are collected too, here we just keep the current values.

## Metrics
|Metric|Description|Unit|Value type|Sampling period|
|------|-----------|----|----------|---------------|
|clouds|Cloudiness|%|int|10m|
|dew_point|Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form|°C|float|10m|
|feels_like|Temperature. This accounts for the human perception of weather.|°C|float|10m|
|humidity|Humidity|%|int|10m|
|pressure|Atmospheric pressure on the sea level|hPa|int|10m|
|temp|Temperature|°C|float|10m|
|uvi|UV index||float|10m|
|visibility|Average visibility, metres. The maximum value of the visibility is 10km|m|int|10m|
|wind_deg|Wind direction|deg|int|10m|
|wind_speed|Wind speed|m/s|float|10m|