# Contributing to Glow

Thank you for considering contributing to Glow! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, constructive, and professional. We're all here to make this integration better for the Home Assistant community.

## How to Contribute

### Reporting Bugs

Before submitting a bug report:
1. Check [existing issues](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/issues)
2. Update to the latest version
3. Verify it's not a configuration issue

When reporting bugs, include:
- **Home Assistant version**
- **Integration version**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Relevant logs** (Settings → System → Logs, filter "glow")
- **Configuration** (sanitize any sensitive data)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check if it's already suggested in [issues](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/issues)
2. Provide clear use cases
3. Explain why it would be useful
4. Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m "Add amazing feature"`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.11 or later
- Home Assistant development environment
- Git

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/glow-sun-exposure-vitamin-d.git
cd glow-sun-exposure-vitamin-d

# Create symlink to your HA config
ln -s $(pwd)/custom_components/glow_vitd ~/.homeassistant/custom_components/

# Or copy for testing
cp -r custom_components/glow_vitd ~/.homeassistant/custom_components/
```

### Testing Changes

1. Restart Home Assistant after code changes
2. Check logs for errors: Settings → System → Logs
3. Test all sensor types
4. Test with and without UV sensor
5. Test during day and night
6. Test configuration changes
7. Test at different latitudes (if possible)

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Add docstrings for functions/classes
- Keep lines under 100 characters
- Use meaningful variable names

Example:
```python
def calculate_exposure_time(
    uv_index: float,
    skin_type: int,
    target_iu: int = 2000,
) -> float:
    """Calculate required sun exposure time.
    
    Args:
        uv_index: Current UV index (0-15)
        skin_type: Fitzpatrick skin type (1-6)
        target_iu: Target vitamin D production in IU
        
    Returns:
        Required exposure time in minutes
    """
    # Implementation
```

## Project Structure

```
custom_components/glow_vitd/
├── __init__.py           # Integration setup & coordinator
├── config_flow.py        # Configuration UI
├── const.py              # Constants and data tables
├── manifest.json         # Integration metadata
├── sensor.py             # Sensor entities
├── strings.json          # UI strings
└── translations/
    └── en.json          # Translations
```

## Key Components

### `__init__.py`
- Integration initialization
- Config entry management
- Data coordinator

### `config_flow.py`
- User configuration interface
- Options flow for settings
- Validation

### `const.py`
- Domain and constants
- Skin type data
- Monthly UV lookup tables

### `sensor.py`
- Sensor entity implementation
- Calculation logic
- State and attribute management

## Testing Checklist

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] All imports are used
- [ ] No debug print statements
- [ ] Error handling is appropriate
- [ ] Logs use appropriate levels (debug/info/warning/error)
- [ ] Integration loads without errors
- [ ] Configuration flow works
- [ ] All 6 sensors are created
- [ ] Calculations are accurate
- [ ] Sensors update correctly
- [ ] Attributes are populated
- [ ] Options flow works
- [ ] Reloading integration works
- [ ] Uninstalling works cleanly

## Adding New Features

### Adding a New Sensor Attribute

1. Add attribute to `extra_state_attributes` in `sensor.py`
2. Update README documentation
3. Test that attribute appears correctly

### Adding Configuration Options

1. Add constant to `const.py`
2. Add to schema in `config_flow.py` (both user and init steps)
3. Update `strings.json` and `translations/en.json`
4. Use in sensor calculations
5. Document in README

### Modifying Calculations

1. Update calculation logic in `sensor.py`
2. Verify against source data (NIH study)
3. Test with various inputs
4. Update comments explaining formula
5. Document changes in commit message

## Documentation

When adding features:

1. Update relevant README sections
2. Add usage examples if applicable
3. Update INSTALLATION.md if setup changes
4. Add comments in code for complex logic
5. Update version in `manifest.json`

## Commit Messages

Use clear, descriptive commit messages:

```
Add support for custom body exposure percentage

- Add CONF_BODY_EXPOSURE to config flow
- Update calculation formula in sensor.py
- Add documentation in README
- Fixes #123
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description with bullet points
- Reference issue numbers

## Release Process

Maintainers will:

1. Update `version` in `manifest.json`
2. Update CHANGELOG
3. Create GitHub release
4. Tag with version number (v1.0.0)

## Questions?

- Open a [Discussion](https://github.com/cinghialino/glow-sun-exposure-vitamin-d/discussions)
- Comment on related issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
