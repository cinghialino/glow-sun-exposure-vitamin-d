"""Constants for Glow Vitamin D Sun Exposure integration."""

DOMAIN = "glow_vitd"
VERSION = "1.0.5"

# Config flow
CONF_TARGET_IU = "target_iu"
CONF_UV_SENSOR = "uv_sensor"
CONF_BODY_EXPOSURE = "body_exposure"

# Defaults
DEFAULT_TARGET_IU = 2000
MIN_TARGET_IU = 1000
MAX_TARGET_IU = 4000
DEFAULT_BODY_EXPOSURE = 25
MIN_BODY_EXPOSURE = 5
MAX_BODY_EXPOSURE = 100

# Minimum UV index for meaningful vitamin D synthesis
MIN_UV_INDEX = 3

# Skin types (Fitzpatrick scale)
SKIN_TYPES = {
    1: {"name": "Type 1 (Very Fair)", "multiplier": 1.0},
    2: {"name": "Type 2 (Fair)", "multiplier": 1.2},
    3: {"name": "Type 3 (Medium)", "multiplier": 1.5},
    4: {"name": "Type 4 (Olive)", "multiplier": 2.0},
    5: {"name": "Type 5 (Brown)", "multiplier": 3.0},
    6: {"name": "Type 6 (Dark Brown/Black)", "multiplier": 4.0},
}

# Monthly average UV index by latitude (simplified model)
# Based on NIH PMC11124381 data
MONTHLY_UV_DATA = {
    # Latitude ranges: 0-15, 15-30, 30-45, 45-60, 60-75, 75-90
    "0-15": [11, 12, 12, 11, 10, 9, 9, 10, 11, 11, 11, 11],  # Tropical
    "15-30": [8, 9, 10, 11, 11, 11, 11, 10, 9, 8, 7, 7],  # Subtropical
    "30-45": [4, 5, 7, 9, 10, 11, 11, 9, 7, 5, 4, 3],  # Temperate
    "45-60": [2, 3, 5, 7, 8, 9, 9, 7, 5, 3, 2, 1],  # Cool temperate
    "60-75": [0, 1, 3, 5, 6, 7, 7, 5, 3, 1, 0, 0],  # Subarctic
    "75-90": [0, 0, 1, 3, 4, 5, 5, 3, 1, 0, 0, 0],  # Arctic/Antarctic
}

# Baseline minutes for Type 1 skin at UV index 7 (summer midday)
# to produce ~2000 IU with 25% body exposure
BASELINE_MINUTES = 15
BASELINE_BODY_EXPOSURE = 25

# State constants
STATE_INSUFFICIENT_UVB = "Insufficient UVB"
STATE_SUN_BELOW_HORIZON = "Sun below horizon"
