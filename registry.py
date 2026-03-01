from tools import IOTTools
from schemas import *

def build_registry(csv_path):
    tools = IOTTools(csv_path)
    
    return {
        "sites": tools.sites,
        "assets": tools.assets,
        "sensors": tools.sensors,
        "history": tools.history,
        "currenttime": tools.currenttime
    }


SCHEMA_REGISTRY = {
    "sites": SitesInput,
    "assets": AssetsInput,
    "sensors": SensorsInput,
    "history": HistoryInput,
    "currenttime": CurrentTimeInput
}