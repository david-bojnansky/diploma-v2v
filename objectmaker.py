from vehicle import Vehicle

class ObjectMaker:
    def vehicle(self, json):
        return Vehicle.fromJson(None, json)
    