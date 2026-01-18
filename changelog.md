# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

- **1.0.0** (2026-01-18): Initial public release
