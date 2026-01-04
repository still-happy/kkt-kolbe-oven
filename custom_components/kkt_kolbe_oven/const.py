"""Constants for the KKT Kolbe Oven integration."""

DOMAIN = "kkt_kolbe_oven"

PLATFORMS = ["switch", "select", "number", "binary_sensor", "sensor"]

CONF_DEVICE_ID = "device_id"
CONF_LOCAL_KEY = "local_key"
CONF_IP_ADDRESS = "ip_address"

# Data Points (DPs) - Using numeric IDs
DP_SWITCH = "105"        # Power on/off
DP_MODE = "101"          # Cooking program
DP_TEMPERATURE = "102"   # Temperature
DP_TIME = "103"          # Timer in minutes
DP_DOOR_STATE = "106"    # Door state
DP_STATUS = "104"        # Status

# Cooking Programs (using format codes from device)
COOKING_PROGRAMS = {
    "f1": "Auftauen",
    "f2": "Oberhitze Grill",
    "f3": "Unterhitze",
    "f4": "Unterhitze Umluft",
    "f5": "Umluft",
    "f6": "Ober-/Unterhitze Umluft",
    "f7": "Ober-/Unterhitze",
    "f8": "Oberhitze Grill Umluft",
    "f9": "Grillen",
    "f10": "Erhitzen",
    "f11": "Warmhalten",
    "f12": "Toasten",
}

# Reverse mapping for program selection
PROGRAM_TO_CODE = {v: k for k, v in COOKING_PROGRAMS.items()}

# Temperature limits
TEMP_MIN = 0
TEMP_MAX = 250

# Time limits (in minutes)
TIME_MIN = 0
TIME_MAX = 1440  # 24 hours
