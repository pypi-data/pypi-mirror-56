
class SimulatorSettings:
    db_session = None
    position_model = None

    @classmethod
    def from_dict(cls, d):
        cls.db_session = d.get('db_session')
        cls.position_model = d.get('position_model')
