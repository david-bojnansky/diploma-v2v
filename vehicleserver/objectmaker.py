from vehicle import Vehicle

class ObjectMaker:
    def foreignVehicle(self, json):
        return Vehicle.fromJson(None, json)
    