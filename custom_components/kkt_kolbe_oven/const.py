"""Constants for the KKT Kolbe Oven integration."""

DOMAIN = "kkt_kolbe_oven"

PLATFORMS = ["switch", "select", "number", "binary_sensor", "sensor"]

CONF_DEVICE_ID = "device_id"
CONF_LOCAL_KEY = "local_key"
CONF_IP_ADDRESS = "ip_address"

# Data Points (DPs)
DP_SWITCH = "kg"
DP_MODE = "wd"
DP_TEMPERATURE = "dw"
DP_TIME = "ds"
DP_DOOR_STATE = "doorstate"
DP_STATUS = "djs"

# Cooking Programs
COOKING_PROGRAMS = {
    "1": "Auftauen",
    "2": "Oberhitze Grill",
    "3": "Unterhitze",
    "4": "Unterhitze Umluft",
    "5": "Umluft",
    "6": "Ober-/Unterhitze Umluft",
    "7": "Ober-/Unterhitze",
    "8": "Oberhitze Grill Umluft",
    "9": "Grillen",
    "10": "Erhitzen",
    "11": "Warmhalten",
    "12": "Toasten",
}

# Reverse mapping for program selection
PROGRAM_TO_CODE = {v: k for k, v in COOKING_PROGRAMS.items()}

# Temperature limits
TEMP_MIN = 0
TEMP_MAX = 250

# Time limits (in minutes)
TIME_MIN = 0
TIME_MAX = 1440  # 24 hours
