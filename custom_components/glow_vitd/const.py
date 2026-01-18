DOMAIN = "glow_vitd"

CONF_TARGET_IU = "target_iu"
CONF_UV_ENTITY = "uv_entity"

DEFAULT_TARGET_IU = 2000

# All-sky (average cloud) base times for white skin (ST I-IV) from NIH Table 3 (minutes)
BASE_TIMES = {
    90: [None] * 12,
    80: [None, None, None, None, None, 14, 14, None, None, None, None, None],
    70: [None, None, None, None, 11, 9, 9, 13, None, None, None, None],
    60: [None, None, None, 12, 8, 6, 6, 8, 14, None, None, None],
    50: [None, None, 12, 8, 6, 5, 5, 6, 8, 15, None, None],
    40: [None, 11, 7, 5, 4, 4, 4, 4, 5, 8, 15, None],
    30: [8, 6, 4, 4, 4, 4, 4, 4, 4, 5, 7, 9],
    20: [5, 4, 3, 4, 5, 4, 4, 4, 3, 4, 5, 5],
    10: [3, 3, 3, 4, 4, 3, 4, 4, 4, 3, 3, 4],
    0: [3, 3, 4, 3, 3, 3, 3, 3, 4, 3, 3, 3],
    -10: [3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 3, 3],
    -20: [4, 3, 3, 4, 5, 6, 6, 4, 4, 4, 4, 4],
    -30: [3, 3, 4, 5, 8, 10, 10, 7, 5, 4, 4, 4],
    -40: [3, 3, 5, 8, 15, None, None, 13, 8, 5, 4, 4],
    -50: [4, 4, 7, 16, None, None, None, None, 13, 7, 5, 4],
    -60: [5, 7, 14, None, None, None, None, None, None, 8, 5, 5],
    -70: [6, 10, None, None, None, None, None, None, None, 7, 5, 5],
    -80: [10, None, None, None, None, None, None, None, None, 12, 7, 7],
    -90: [None] * 12
}

# Skin multipliers relative to type 2 (NILU)
SKIN_MULTIPLIERS = {1: 0.8, 2: 1.0, 3: 1.2, 4: 1.8, 5: 2.4, 6: 4.0}

# UV formula constant
UV_CONSTANT = 36.0
