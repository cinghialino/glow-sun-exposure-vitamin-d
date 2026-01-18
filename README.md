# Vitamin D Sun Exposure Integration for Home Assistant

This custom integration calculates the estimated minutes of midday sun exposure needed to maintain sufficient Vitamin D levels, based on your Home Assistant location (latitude), current month, and configured skin type (Fitzpatrick scale 1-6). It creates a sensor entity showing the minutes required. Calculations are only performed when the sun is above the horizon (using HA's sun integration); otherwise, the sensor state is "unknown."

Inspired by the [Sunshine Calendar chart](https://www.evergreen-life.co.uk/wp-content/uploads/2022/10/Vitamin-D-Sunshine-Calendar-for-worldwide-locations.png) and enhanced with data from [NIH UVB exposure studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC11124381). Assumes 35% body exposure (e.g., shorts + T-shirt) for maintenance of ~50 nmol/L 25OHD levels.

## Features
- Sensor: `sensor.vitamin_d_exposure_minutes` (unit: minutes)
- Accounts for Fitzpatrick skin types (1-6), with scaling for darker skin.
- Updates hourly, but only if sun is up.
- "W" (Vitamin D Winter) periods show "Insufficient UVB" if no production possible.

## Installation
1. Install via HACS:
   - In HACS > Integrations, click the three dots > Custom repositories.
   - Add this repo URL: `https://github.com/yourusername/home-assistant-vitamin-d`
   - Category: Integration
   - Install the integration.
2. Restart Home Assistant.
3. Go to Settings > Devices & Services > Add Integration > Search for "Vitamin D Sun Exposure".
4. Configure your skin type (1-6) in the setup flow.

Manual install: Copy the `custom_components/vitamin_d` folder to your HA `config/custom_components/` directory.

## Configuration
During setup, select your Fitzpatrick skin type:
- 1: Very fair, always burns
- 2: Fair, burns easily
- 3: Medium, burns moderately
- 4: Olive, burns minimally
- 5: Brown, rarely burns
- 6: Black, never burns

No YAML config needed – all via UI. If you need to change skin type later, delete and re-add the integration.

## Example Usage
- In Lovelace, add a entities card with `sensor.vitamin_d_exposure_minutes`.
- Automation idea: Notify if minutes < 30 and sun is up – time to get outside!

## Screenshots
![Sensor Example](./images/sensor_example.png)
*Sensor showing 15 minutes needed (e.g., for skin type 3 at 40°N in summer).*

![Config Flow](./images/config_flow.png)
*Setup screen for selecting skin type.*

## Development & Credits
- Built with Home Assistant core scaffold.
- Data sourced from NIH PMC11124381 and the provided sunshine calendar.
- Issues/PRs welcome!

If you encounter issues, check HA logs for "vitamin_d".
