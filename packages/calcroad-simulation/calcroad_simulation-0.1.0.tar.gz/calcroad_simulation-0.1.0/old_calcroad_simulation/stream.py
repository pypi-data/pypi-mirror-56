from itertools import groupby
from operator import attrgetter
from .settings import SimulatorSettings

class SimulationStream:
    @classmethod
    def dump_vehicule(cls, vehicule):
        return {
            "type": "Feature",
            "properties": {
                "id": vehicule.id,
                "speed": vehicule.speed
            },
            "geometry": {
                "coordinates": [vehicule.lat, vehicule.lng],
                "type": "Point"
            }
            
        }
        
    @classmethod
    def dump(cls, map_id, start_time, limit=30):
        end_time = start_time + limit
        
        vehicules = SimulatorSettings.db_session.query(
            SimulatorSettings.position_model
        ).filter(
            SimulatorSettings.position_model.map_id==map_id,
            SimulatorSettings.position_model.time>=start_time, 
            SimulatorSettings.position_model.time<=end_time
        ).order_by(
            SimulatorSettings.position_model.time, 
            SimulatorSettings.position_model.id
        ).all()
        
        
        positions = []
        
        k = 0
        vehicules_by_time = dict(
            (timestamp, list(map(cls.dump_vehicule, vehicules_by_time)))
            for timestamp, vehicules_by_time in groupby(
                vehicules, attrgetter('time')))
        
        return [{
            'type': 'FeatureCollection',
            'properties': {
              'time': ts  
            },
            'features': vehicules_by_time.get(ts, [])
        } for ts in range(start_time, start_time+limit)]
