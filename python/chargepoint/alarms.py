from json import dumps

from s3l_utils.enum import MultiValueEnum


class AlarmEnum(MultiValueEnum):
    """ChargePoint alarm enum"""

    BOOT_UP = "Boot up"
    BOOTUP_DUE_TO_POWER_ON = "Bootup Due to POWER ON"
    BOOTUP_DUE_TO_SOFT_RESET = "Bootup Due to SOFT RESET"
    BOOTUP_DUE_TO_SWITCH = "Bootup Due to SWITCH"
    BOOTUP_DUE_TO_WATCHDOG = "Bootup Due to WATCHDOG"
    CHADEMO_CONTROL_LOOP_DETECTED_FAULT = "CHAdeMO control loop detected fault (39)"
    CHARGER_FAULT_CONTACT_TRITIUM = "Charger Fault - contact Tritium (28)"
    CIRCUIT_SHARING_REDUCED = "Circuit Sharing Current Reduced"
    CIRCUIT_SHARING_RESTORED = "Circuit Sharing Current Restored"
    COMMUNICATION_TIMEOUT = "Communication timeout. (62)", "Communication timeout. (63)"
    DATA_PARTITION_FULL = "Data Partition Full"
    EARTH_FAULT_STATION_IN_SERVICE = "Earth Fault Station In Service"
    EARTH_FAULT_STATION_OUT_OF_SERVICE = "Earth Fault Station Out Of Service"
    FAULT_CLEARED = "Fault Cleared"
    FCHECK_ERROR = "FCheck Error"
    GFCI_HARD_TRIP = "GFCI Hard Trip"
    GFCI_SOFT_TRIP = "GFCI Soft Trip"
    GRACE_SESSIONS_EXCEEDED = "Grace Sessions Exceeded"
    HARDWARE_FAULT = "Hardware Fault"
    HARDWARE_FAULT_STATION_OUT_OF_SERVICE = "Hardware Fault Station Out Of Service"
    IP_MISMATCH_DETECTED = "IP Mismatch Detected"
    MAINTENANCE_REQUIRED = "Maintenance Required"
    PILOT_CURRENT_LEVEL_EXCEEDED = "Pilot current level exceeded"
    PILOT_UNREACHABLE = "Pilot Unreachable (18)"
    POWERED_OFF = "Powered Off"
    REACHABLE = "Reachable"
    RELAY_STUCK_CLOSE = "Relay Stuck Close"
    RFID_UPDATE_FAILED = "RFID Update Failed"
    SOFT_ESTOP = "Emergency Stop button pressed - No circuit breaker Trip fired (Soft E-Stop) (188)"
    STATION_NOT_ACTIVATED = "Station Not Activated"
    TAMPER_DETECT = "Tamper Detect"
    UNKNOWN_RFID = "Unknown RFID"
    UNREACHABLE = "Unreachable", "EVSE Unreachable"
    VEHICLE_FAULT = "Vehicle fault (50)"
    VENTILATION_FAULT = "Ventilation Fault"

    @classmethod
    @property
    def faults(cls):
        return (
            cls.CHADEMO_CONTROL_LOOP_DETECTED_FAULT,
            cls.CHARGER_FAULT_CONTACT_TRITIUM,
            cls.DATA_PARTITION_FULL,
            cls.EARTH_FAULT_STATION_IN_SERVICE,
            cls.EARTH_FAULT_STATION_OUT_OF_SERVICE,
            cls.HARDWARE_FAULT_STATION_OUT_OF_SERVICE,
            cls.HARDWARE_FAULT,
            cls.MAINTENANCE_REQUIRED,
            cls.PILOT_UNREACHABLE,
            cls.RELAY_STUCK_CLOSE,
            cls.TAMPER_DETECT,
            cls.VENTILATION_FAULT,
            cls.SOFT_ESTOP
        )

    @classmethod
    @property
    def boot(cls):
        return (
            cls.BOOT_UP,
            cls.BOOTUP_DUE_TO_POWER_ON,
            cls.BOOTUP_DUE_TO_SOFT_RESET,
            cls.BOOTUP_DUE_TO_SWITCH,
            cls.BOOTUP_DUE_TO_WATCHDOG,
        )
