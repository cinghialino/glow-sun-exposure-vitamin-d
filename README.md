# Glow: Sun Exposure Calculator for Vitamin D (Home Assistant Integration)

This integration estimates minutes of sun exposure needed for sufficient Vitamin D, based on your location (latitude), month, Fitzpatrick skin type (1-6), and optional real-time UV index from a weather sensor. Creates 6 sensors (one per skin type) showing minutes required. Only calculates when sun is above horizon; otherwise, "unknown."

Based on [NIH UVB exposure study (PMC11124381)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11124381/) Table 3 (all-sky/average cloud conditions) and the [original sunshine calendar](https://www.evergreen-life.co.uk/wp-content/uploads/2022/10/Vitamin-D-Sunshine-Calendar-for-worldwide-locations.png). Assumes ~25% body exposure for ~50 nmol/L maintenance. Target IU configurable (default 2000).

## Features
- 6 Sensors: `sensor.glow_type_1_minutes` to `sensor.glow_type_6_minutes` (unit: min)
- Skin multipliers from NILU data.
- Configurable target Vitamin D dose (1000-4000 IU).
- Optional UV index for real-time adjustments (overrides monthly average).
- Updates every 30 min if sun up.
- "Insufficient UVB" for low-UV periods.
- Sensor attributes: `recommended_time` (e.g., "Midday (11 AM - 3 PM local time)").

## Installation
1. Via HACS: Add repo ```https://github.com/cinghialino/glow-sun-exposure-vitamin-d``` as Integration.
2. Restart HA.
3. Add via Settings > Devices & Services > "Glow: Sun Exposure for Vitamin D".
4. Configure target IU and optional UV sensor.

Manual: Copy ```custom_components/glow_vitd``` to your config.

## Configuration
- **Target IU**: Slider (default 2000 IU).
- **UV Sensor**: Select a sensor (e.g., `sensor.openuv_current_uv_index`).
- Edit via Integration Options.

Disable unused sensors in entity registry.

## Example Usage
- Automation: If `sensor.glow_type_3_minutes` < 20 and sun up, notify "Get some glow!"
- With UV: Adjusts dynamically.

## Lovelace Examples
Add to your dashboard YAML:

### Basic Entities Card
```yaml
type: entities
entities:
  - entity: sensor.glow_type_3_minutes
    name: My Skin Type (Type 3)
  - entity: sensor.glow_type_5_minutes
    name: Partner's Skin Type (Type 5)
title: Vitamin D Exposure
```

### Advanced Mushroom Chips Card (requires mushroom-card custom component)
```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: sensor.glow_type_3_minutes
    icon: mdi:sun-wireless
    content_info: name
    tap_action:
      action: more-info
  - type: conditional
    conditions:
      - entity: sensor.glow_type_3_minutes
        state_not: unknown
        state_not: 'Insufficient UVB'
    chip:
      type: template
      content: '{{ states(''sensor.glow_type_3_minutes'') }} min today'
      icon: mdi:clock-outline
      icon_color: '{{ ''green'' if states(''sensor.glow_type_3_minutes'') | int < 30 else ''orange'' }}'
```
This shows exposure time with color-coded urgency if sun is up.

### Screenshots
soon

### Development & Credits

- Uses HA sun and UV sensor.
- Data: NIH PMC11124381 (all-sky), NILU models.
- Issues/PRs welcome!
