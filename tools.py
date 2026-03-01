import pandas as pd
import os
import json
from datetime import datetime

TEMP_DIR = "temp_outputs"
os.makedirs(TEMP_DIR, exist_ok=True)

class IOTTools:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
    
    def _save_json(self, data, prefix):
        file_name = f"{prefix}_{datetime.now().timestamp()}.json"
        file_path = os.path.join(TEMP_DIR, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return file_path
    
    def sites(self):
        sites = self.df['site_name'].unique().tolist()
        return {"sites": sites}
    
    def assets(self, site_name):
        filtered = self.df[self.df["site_name"] == site_name]
        assets = filtered["asset_id"].unique().tolist()
        file_path = self._save_json(assets, "assets")
        return{"site_name": site_name, "total_assets": len(assets), "file_path": file_path, "message": f"{len(assets)} assets found for {site_name}"}
    
    def sensors(self, site_name, asset_id):
        filtered = self.df[(self.df["site_name"] == site_name) & (self.df["asset_id"] == asset_id)]
        sensors = filtered["sensor_name"].unique().tolist()
        file_path = self._save_json(sensors, "sensors")
        return{"site_name": site_name, "asset_id": asset_id, "total_sensors": len(sensors), "file_path": file_path, "message": f"{len(sensors)} sensors found"}
    
    def history(self, site_name, asset_id, start, final, sensor_list= None):
        start = pd.to_datetime(start)
        final = pd.to_datetime(final)
        filtered = self.df[(self.df["site_name"] == site_name) & (self.df["asset_id"] == asset_id) & (self.df["timestamp"] >= start) & (self.df["timestamp"] <= final)]
        if sensor_list: 
            filtered = filtered[filtered["sensor_name"].isin(sensor_list)]
        data = filtered.to_dict(orient="records")
        file_path = self._save_json(data, "history")
        return {"site_name": site_name, "asset_id": asset_id, "start": str(start), "final": str(final), "total_observations": len(data), "file_path": file_path}
    
    def currenttime(self):
        return {"current_time": datetime.now().isoformat()}
    
    def jsonreader(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)



        
        
