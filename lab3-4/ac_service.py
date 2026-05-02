import grpc
from laboratory import air_conditioner_pb2, air_conditioner_pb2_grpc
from google.protobuf import empty_pb2


class ACService(air_conditioner_pb2_grpc.ACServiceServicer):
    def __init__(self, database):
        self.db = database
        self.TYPE = "AC"
    
    def GetACStatus(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        
        print("Status sent")
        if "basic" in device:
            return air_conditioner_pb2.ACStatus(
                id=request,
                is_on=device["is_on"],
                current_temp=device["current_temp"],
                target_temp=device["target_temp"]
            )
        
        return air_conditioner_pb2.ACStatus(
            id=request,
            is_on=device["is_on"],
            current_temp=device["current_temp"],
            target_temp=device["target_temp"],
            advanced=air_conditioner_pb2.AdvancedACData(
                fan_mode=device["advanced"]["fan_mode"],
                current_humidity=device["advanced"]["current_humidity"],
                target_humidity=device["advanced"]["target_humidity"]
            )
        )
    def EnableAC(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        
        device["is_on"] = True
        print("AC enabled")
        return empty_pb2.Empty()
    
    def DisableAC(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        
        device["is_on"] = False
        print("AC disabled")
        return empty_pb2.Empty()
    