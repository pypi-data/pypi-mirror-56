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
    def dump_vehicules(cls, vehicules):
        return [
            {
                'type': 'FeatureGroup',
                'features': list(map(cls.dump_vehicule, vehicule)) 
            }
            for k, vehicule in groupby(vehicules, attrgetter('time'))
        ]
        
    @classmethod
    def dump(cls, start_time=28800, limit=30):
        end_time = start_time + limit
        
        vehicules = SimulatorSettings.db_session.query(
            SimulatorSettings.position_model
        ).filter(
            SimulatorSettings.position_model.time>=start_time, 
            SimulatorSettings.position_model.time<=end_time
        ).order_by(
            SimulatorSettings.position_model.time, 
            SimulatorSettings.position_model.id
        ).all()
        
        return cls.dump_vehicules(vehicules)
        