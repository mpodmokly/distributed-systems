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
                target_temp=device["target_temp"],
                basic=air_conditioner_pb2.BasicACData()
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
    
    def SetACTemp(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "AC must be enabled to set temp"
            )
        if request.target_temp < 5 or request.target_temp > 25:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, "Temp out of range")
        
        device["target_temp"] = request.target_temp
        print("Target temp set")
        return empty_pb2.Empty()
    
    def SetACFan(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "AC must be enabled to set fan mode"
            )
        if not "advanced" in device:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not advanced type"
            )
        
        device["advanced"]["fan_mode"] = air_conditioner_pb2.FanMode.Name(
            request.fan_mode
        )
        print("Fan mode set")
        return empty_pb2.Empty()
    
    def SetACHumidity(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        if not device["type"] == self.TYPE:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not AC"
            )
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "AC must be enabled to set humidity"
            )
        if not "advanced" in device:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not advanced type"
            )
        if request.target_humidity < 0 or request.target_humidity > 100:
            context.abort(
                grpc.StatusCode.OUT_OF_RANGE,
                "Humidity out of range"
            )
        
        device["advanced"]["target_humidity"] = request.target_humidity
        print("Target humidity set")
        return empty_pb2.Empty()
