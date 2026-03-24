# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.6] - 2026-03-23

### Fixed
- Fix icon transparency — corners had opaque light-gray fill instead of true transparency

## [1.0.5] - 2026-03-23

### Added
- **Automated test suite** with 68 tests covering calculations, coordinator, monthly UV lookup, constants, and edge cases
- **Translations**: Italian (it), Spanish (es), German (de)

### Fixed
- `iot_class` casing in `hacs.json` — was `"Calculated"`, now `"calculated"` to match `manifest.json`

## [1.0.4] - 2026-03-23

### Changed
- **Refactored**: All calculations now run in the coordinator instead of being duplicated across each sensor class. Sensors read from shared coordinator data, reducing redundant work and improving maintainability.
- **Refactored**: Extracted shared device info and coordinator listener logic into a `GlowBaseSensor` base class, eliminating boilerplate across all sensor classes.
- Minimum UV index threshold is now an explicit constant (`MIN_UV_INDEX = 3`).
- Version string is now a single constant (`VERSION`) used consistently across device info and manifest.

### Added
- **Configurable body exposure percentage** (5-100%, default 25%). Previously hardcoded at 25%. Available in both initial setup and options flow.
- **Latitude > 75° support**: Added `"75-90"` range to the monthly UV lookup table for Arctic/Antarctic locations.
- `configuration_url` in device info linking to the GitHub documentation.

### Removed
- Deleted unused `options_flow.py` (dead code referencing non-existent `CONF_UV_ENTITY`). The options flow in `config_flow.py` was already the active implementation.

### Fixed
- **Inconsistent `sw_version`**: Device info previously showed "1.0.2" in some sensors and "1.0.0" in others. Now all sensors use the same `VERSION` constant.
- Device name is now consistently "Glow: Sun Exposure for Vitamin D" across all sensors (was "Glow" in some).

## [1.0.2] - 2026-01-18

### Changed
- **BREAKING**: Changed entity IDs for better naming consistency:
  - Minutes sensors: `sensor.glow_type_X` → `sensor.glow_sun_exposure_type_X`
  - Status sensors: `sensor.glow_type_X_status` → `sensor.glow_sun_exposure_type_X_status`
- Sensor display names remain unchanged (e.g., "Type 1", "Type 1 status")

### Added
- **UV Index sensor** (`sensor.glow_sun_exposure_uv_index`): Displays the current UV index being used in calculations
  - Shows real-time value from configured UV sensor, or monthly average as fallback
  - Attributes show source (UV sensor or monthly average) and sensor entity
- **Calculation Method sensor** (`sensor.glow_sun_exposure_calculation_method`): Shows data source
  - Displays "Real-time UV sensor", "Monthly average for latitude", or "Monthly average (sensor unavailable)"
  - Helps troubleshoot when UV sensor isn't working
  - Attributes include target IU, latitude, and UV sensor entity info
- Integration icon for better visual identification in Home Assistant
- Ko-fi donation link in README for project support

### Fixed
- All README examples updated with correct entity IDs
- Documentation now matches actual sensor entity IDs

### Migration Notes
If upgrading from 1.0.1:
- Entity IDs have changed again - update your automations and dashboards
- Old: `sensor.glow_type_3` → New: `sensor.glow_sun_exposure_type_3`
- Old: `sensor.glow_type_3_status` → New: `sensor.glow_sun_exposure_type_3_status`
- Two new utility sensors added: UV Index and Calculation Method

## [1.0.1] - 2026-01-18

### Changed
- **BREAKING**: Renamed minutes sensors from "Type X minutes" to just "Type X" (using unit definition instead)
- Sensor entity IDs changed from `sensor.glow_type_X_minutes` to `sensor.glow_type_X`
- Fixed sun position detection to use `sun.sun` entity directly (more reliable)

### Added
- 6 new status sensors (one per skin type): `sensor.glow_type_X_status`
- Status sensors provide human-readable descriptions:
  - "Sun below horizon"
  - "Insufficient UVB"
  - "Quick exposure needed" (< 15 min)
  - "Moderate exposure needed" (15-30 min)
  - "Extended exposure needed" (30-60 min)
  - "Long exposure needed" (> 60 min)
- Status sensors include `minutes_needed` and `uv_index` attributes
- Debug logging for sun position checks

### Fixed
- Sun position detection now works correctly during daytime
- Integration now properly detects when sun is above horizon

### Migration Notes
If upgrading from 1.0.0:
- Minutes sensor entity IDs have changed
- Update your automations and dashboards to use new entity IDs
- Old entity IDs: `sensor.glow_type_X_minutes`
- New entity IDs: `sensor.glow_type_X` (minutes) and `sensor.glow_type_X_status`

## [1.0.0] - 2026-01-18

### Added
- Initial release of Glow: Sun Exposure for Vitamin D integration
- 6 sensor entities for Fitzpatrick skin types 1-6
- Configurable target Vitamin D production (1000-4000 IU)
- Optional UV index sensor integration for real-time calculations
- Location-based monthly UV average calculations
- Sun position awareness (only calculates when sun is above horizon)
- Comprehensive sensor attributes including:
  - Skin type information
  - UV index used in calculation
  - Calculation method (real-time vs monthly average)
  - Recommended exposure time
  - Target IU and body exposure percentage
- Configuration flow with validation
- Options flow for adjusting settings after setup
- Support for HACS installation
- Comprehensive documentation including:
  - README with usage examples
  - Installation guide
  - Contributing guidelines
  - Medical disclaimers and safety information
- Based on NIH study (PMC11124381) and NILU skin type data
- Special states for insufficient UVB and sun below horizon

### Features
- Automatic calculation updates every 30 minutes when sun is up
- Proper handling of edge cases (polar regions, equator, winter)
- Integration with Home Assistant sun integration
- Device grouping for all sensors
- Entity registry support for enabling/disabling sensors
- Full Home Assistant 2023.8.0+ compatibility

### Technical
- Proper config entry setup with coordinator pattern
- Type hints throughout codebase
- Error handling and logging
- Translations support (English included)
- Home Assistant quality standards compliance

### Documentation
- Complete README with examples
- Detailed installation instructions
- Usage examples for Lovelace cards
- Automation examples
- Troubleshooting guide
- API documentation in code comments

## [Unreleased]

### Planned Features
- Support for custom body exposure percentages
- Historical tracking and graphing
- Seasonal recommendations
- Integration with calendar for optimal exposure times
- Multi-language support
- Cloud cover adjustments (when UV sensor unavailable)
- Age-based efficiency adjustments
- Supplementation tracking and recommendations

### Under Consideration
- Mobile app notifications
- Apple Watch / Wear OS complications
- Location-specific cloud cover data integration
- Skin cancer risk assessment
- Personalized recommendations based on blood test results
- Integration with fitness trackers for outdoor activity correlation

---

## Version History

- **1.0.5** (2026-03-23): Automated tests, translations (it/es/de), iot_class fix
- **1.0.4** (2026-03-23): Refactored coordinator, configurable body exposure, high-latitude support
- **1.0.0** (2026-01-18): Initial public release
