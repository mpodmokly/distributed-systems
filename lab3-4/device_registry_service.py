from laboratory import common_pb2, common_pb2_grpc


class DeviceRegistryService(common_pb2_grpc.DeviceRegistryServiceServicer):
    def __init__(self, database):
        self.db = database
    
    def ListDevices(self, request, context):
        devices = []

        for device_id in self.db:
            devices.append(common_pb2.DeviceID(id=device_id))
        
        print("Devices list sent")
        return common_pb2.DevicesList(devices=devices)
