# Glow: Sun Exposure Calculator for Vitamin D

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/cinghialino/glow-sun-exposure-vitamin-d.svg)](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/releases)
[![License](https://img.shields.io/github/license/cinghialino/glow-sun-exposure-vitamin-d.svg)](LICENSE)

A Home Assistant custom integration that calculates the estimated minutes of midday sun exposure needed to maintain sufficient Vitamin D levels based on your location, time of year, skin type (Fitzpatrick scale 1-6), and optional real-time UV index data.

## ⚠️ Important Medical Disclaimer

**THIS IS NOT MEDICAL ADVICE.** This integration is for informational and educational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before making any decisions about sun exposure, supplementation, or health-related matters.

**Skin Cancer Risk:** Excessive sun exposure increases the risk of skin cancer. This tool does not account for individual risk factors such as:
- Personal or family history of skin cancer
- Number and type of moles
- Previous sunburns
- Medications that increase photosensitivity
- Other medical conditions

**Individual Variation:** Vitamin D production varies significantly between individuals due to age, weight, overall health, and other factors not captured by this calculator.

## Features

- **6 Automatic Sensors**: Creates one sensor for each Fitzpatrick skin type (Type 1-6)
- **Smart Calculations**: Based on NIH research ([PMC11124381](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11124381/)) and NILU skin type data
- **Real-time UV Integration**: Optionally use a UV index sensor for dynamic calculations
- **Location-Aware**: Uses your Home Assistant latitude to determine monthly UV averages
- **Configurable**: Set your target Vitamin D production (1000-4000 IU)
- **Sun-Aware**: Only calculates when sun is above horizon; shows appropriate status otherwise

## How It Works

The integration calculates exposure time based on:

1. **Skin Type Multiplier**: Type 1 (fair) = 1.0×, Type 6 (dark) = 4.0×
2. **UV Index**: Real-time from sensor OR monthly average for your latitude
3. **Target Vitamin D**: Your configured daily IU goal (default: 2000 IU)
4. **Body Exposure**: Assumes 25% (face, arms, legs) for maintenance of ~50 nmol/L

**Formula**: `minutes = 15 × (target_iu / 2000) × skin_multiplier × (7 / uv_index)`

Where 15 minutes is the baseline for Type 1 skin at UV index 7 to produce 2000 IU.

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository URL: `https://github.com/cinghialino/glow-sun-exposure-vitamin-d`
5. Category: "Integration"
6. Click "Add"
7. Click "Install" on the Glow integration
8. Restart Home Assistant
9. Go to Settings → Devices & Services → Add Integration
10. Search for "Glow" and follow the setup wizard

### Manual Installation

1. Download the latest release from GitHub
2. Copy the `custom_components/glow_vitd` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration
5. Search for "Glow" and follow the setup wizard

## Configuration

### Initial Setup

When adding the integration, you'll configure:

- **Target Vitamin D (IU)**: Choose between 1000-4000 IU
  - 1000 IU: Minimal maintenance
  - 2000 IU: Standard maintenance (default)
  - 3000-4000 IU: Higher targets for deficiency correction
  
- **UV Index Sensor** (Optional): Select a UV sensor entity
  - Examples: `sensor.openuv_current_uv_index`, `sensor.accuweather_uv_index`
  - If not provided, uses monthly averages for your latitude

### Adjusting Settings

You can change settings anytime:

1. Go to Settings → Devices & Services
2. Find "Glow: Sun Exposure for Vitamin D"
3. Click "Configure"
4. Adjust your settings
5. Click "Submit"

### Sensor Management

The integration creates 6 sensors:
- `sensor.glow_type_1_minutes` - Very Fair skin
- `sensor.glow_type_2_minutes` - Fair skin
- `sensor.glow_type_3_minutes` - Medium skin
- `sensor.glow_type_4_minutes` - Olive skin
- `sensor.glow_type_5_minutes` - Brown skin
- `sensor.glow_type_6_minutes` - Dark Brown/Black skin

**Tip**: Disable unused skin types in Settings → Devices & Services → Glow → Entities to reduce clutter.

## Sensor Attributes

Each sensor provides these attributes:

- `skin_type`: Numeric type (1-6)
- `skin_type_name`: Full description (e.g., "Type 3 (Medium)")
- `recommended_time`: "Midday (11 AM - 3 PM local time)"
- `target_iu`: Your configured IU goal
- `body_exposure`: "25% (face, arms, legs)"
- `uv_index_used`: Current UV index in calculation
- `calculation_method`: "real-time UV sensor" or "monthly average for latitude"
- `status`: Special states like "Insufficient UVB" or "Sun below horizon"

## Sensor States

Sensors display:
- **Numeric value** (e.g., `12.5`): Minutes of midday sun exposure needed
- **`unknown`**: Sun is below horizon OR insufficient UVB (< 3 UV index)
- **`unavailable`**: Integration error or loading

Check the `status` attribute for details when state is `unknown`.

## Usage Examples

### Basic Dashboard Card

```yaml
type: entities
title: Daily Sun Exposure for Vitamin D
entities:
  - entity: sensor.glow_type_3_minutes
    name: My Skin Type
    icon: mdi:white-balance-sunny
  - type: attribute
    entity: sensor.glow_type_3_minutes
    attribute: recommended_time
    name: Best Time
  - type: attribute
    entity: sensor.glow_type_3_minutes
    attribute: uv_index_used
    name: Current UV Index
```

### Automation: Morning Sun Reminder

```yaml
alias: "Sun Exposure Reminder"
trigger:
  - platform: time
    at: "10:00:00"
condition:
  - condition: numeric_state
    entity_id: sensor.glow_type_3_minutes
    below: 30
  - condition: state
    entity_id: sun.sun
    state: "above_horizon"
  - condition: numeric_state
    entity_id: sensor.glow_type_3_minutes
    above: 0
action:
  - service: notify.mobile_app
    data:
      title: "Get Your Glow! ☀️"
      message: >
        You need {{ states('sensor.glow_type_3_minutes') }} minutes 
        of midday sun today for your Vitamin D. UV index: 
        {{ state_attr('sensor.glow_type_3_minutes', 'uv_index_used') }}
```

### Conditional Card (Show Only When Sun is Up)

```yaml
type: conditional
conditions:
  - entity: sensor.glow_type_3_minutes
    state_not: "unknown"
card:
  type: glance
  title: Sun Exposure Needed Today
  entities:
    - entity: sensor.glow_type_3_minutes
      name: Minutes
    - entity: sun.sun
      name: Sun Position
```

### Mushroom Chips Card (requires mushroom custom card)

```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: sensor.glow_type_3_minutes
    icon: mdi:sun-wireless
    content_info: state
  - type: template
    content: >
      {% if states('sensor.glow_type_3_minutes') != 'unknown' %}
        UV: {{ state_attr('sensor.glow_type_3_minutes', 'uv_index_used') }}
      {% else %}
        Sun down
      {% endif %}
    icon: mdi:weather-sunny-alert
```

## Understanding Your Results

### UV Index Guide

- **0-2**: No protection needed (Insufficient for Vitamin D)
- **3-5**: Moderate - wear sunscreen after calculated minutes
- **6-7**: High - limit exposure, use protection
- **8-10**: Very High - minimize midday exposure
- **11+**: Extreme - avoid midday sun

### Exposure Guidelines

- **Always** avoid sunburn - it significantly increases cancer risk
- The calculated time is for **unprotected skin**
- After achieving your minutes, cover up or use sunscreen (SPF 30+)
- Split exposure across multiple days if needed
- **Never** exceed recommended time without protection
- Consider supplements if UV index regularly below 3

### Seasonal Considerations

- **Winter (High Latitudes)**: Often shows "Insufficient UVB" - supplementation recommended
- **Summer**: Shorter exposure times needed, higher UV risk
- **Equatorial**: Consistent year-round, always use sun protection after exposure
- **Polar Regions**: Extended periods of no UVB (polar night) - supplementation essential

## Data Sources & Methodology

This integration is based on:

1. **NIH Study**: [Ultraviolet B Exposure: A Holistic Approach](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11124381/) (PMC11124381)
2. **NILU Skin Type Models**: Fitzpatrick scale multipliers for vitamin D production
3. **Evergreen Life Sunshine Calendar**: Monthly UV validation data

### Assumptions & Limitations

- Assumes 25% body surface area exposed (face, arms, legs)
- Calculated for midday sun (11 AM - 3 PM local solar time)
- Targets ~50 nmol/L serum 25(OH)D maintenance
- Does not account for:
  - Cloud cover (unless using real-time UV sensor)
  - Air pollution
  - Altitude
  - Ground reflection (snow, water, sand)
  - Glass/window filtering
  - Age-related efficiency loss
  - Obesity or malabsorption conditions
  - Medications affecting vitamin D metabolism

## Troubleshooting

### Integration Won't Install

1. Ensure Home Assistant is version 2023.8.0 or later
2. Check that `custom_components/glow_vitd/` has all required files
3. Restart Home Assistant fully (not just reload)
4. Check logs: Settings → System → Logs (filter for "glow")

### Sensors Show "Unavailable"

1. Check that your Home Assistant location (latitude/longitude) is set
2. Verify the sun integration is working: `sun.sun` entity exists
3. If using UV sensor, check it's available and has numeric state
4. Restart the integration: Settings → Devices & Services → Glow → "..." → Reload

### Sensors Always Show "Unknown"

- **Sun below horizon**: Normal - wait for sunrise
- **Insufficient UVB**: UV index < 3, common in winter
- Check `status` attribute for details

### Wrong Calculations

1. Verify your Home Assistant location is correct
2. If using UV sensor, confirm it reports accurate values (0-15 range)
3. Check that time zone is set correctly
4. Review the calculation in sensor attributes

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Clone the repo
git clone https://github.com/cinghialino/glow-sun-exposure-vitamin-d.git

# Symlink to your HA config
ln -s $(pwd)/custom_components/glow_vitd ~/.homeassistant/custom_components/

# Restart HA after changes
```

## Support

- **Issues**: [GitHub Issues](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/discussions)
- **Documentation**: This README and code comments

## Changelog

### Version 1.0.0 (2026-01-18)
- Initial release
- 6 skin type sensors
- Configurable target IU (1000-4000)
- Optional UV sensor integration
- Location-based monthly UV averages
- Sun position awareness
- Full HACS support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- NIH for the comprehensive UVB exposure research
- NILU for skin type modeling data
- Evergreen Life for the sunshine calendar visualization
- Home Assistant community for integration development support

## Disclaimer

Again, for emphasis: **This tool is for educational purposes only.** Vitamin D status should be monitored by healthcare professionals through blood tests (25(OH)D levels). Sun exposure carries risks. Use sun protection after the calculated exposure time. When in doubt, consult your doctor. Thanks.

---

**Made with ☀️ for the Home Assistant community**
