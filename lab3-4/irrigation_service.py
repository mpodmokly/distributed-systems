import grpc
from laboratory import irrigation_pb2, irrigation_pb2_grpc
from google.protobuf import empty_pb2


class IrrigationService(irrigation_pb2_grpc.IrrigationServiceServicer):
    def __init__(self, database):
        self.db = database
        self.IRRIGATION = "IRRIGATION"
    
    def GetIrrigationStatus(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )

        if "water_type" in device:
            return irrigation_pb2.IrrigationStatus(
                id=request,
                is_on=device["is_on"],
                light=irrigation_pb2.LightMode.Value(device["light"]),
                water_type=irrigation_pb2.WaterIrrigationData(
                    water_flow=device["water_type"]["water_flow"]
                )
            )
        
        return irrigation_pb2.IrrigationStatus(
            id=request,
            is_on=device["is_on"],
            light=irrigation_pb2.LightMode.Value(device["light"]),
            fertilizer_type=irrigation_pb2.FertilizerIrrigationData(
                fertilizer_ratio=device["fertilizer_type"]["fertilizer_ratio"]
            )
        )
    
    def EnableIrrigation(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]

        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )
        
        device["is_on"] = True
        return empty_pb2.Empty()
    
    def DisableIrrigation(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        
        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )
        
        device["is_on"] = False
        return empty_pb2.Empty()
    
    def SetLightMode(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        
        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )
        
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Irrigation must be enabled to set light mode"
            )

        device["light"] = irrigation_pb2.LightMode.Name(
            request.light
        )
        return empty_pb2.Empty()
    
    def SetWaterFlow(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        
        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )
        
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Irrigation must be enabled to set water flow"
            )
        
        if not "water_type" in device:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not water irrigation type"
            )
        
        if request.water_flow < 0 or request.water_flow > 1000:
            context.abort(
                grpc.StatusCode.OUT_OF_RANGE,
                "Water flow out of range"
            )

        device["water_type"]["water_flow"] = request.water_flow
        return empty_pb2.Empty()
    
    def SetFertilizerRatio(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        
        if not device["type"] == self.IRRIGATION:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not irrigation"
            )
        
        if not device["is_on"]:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Irrigation must be enabled to set fertilizer ratio"
            )
        
        if not "fertilizer_type" in device:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Device is not fertilizer irrigation type"
            )
        
        if request.fertilizer_ratio < 0 or request.fertilizer_ratio > 100:
            context.abort(
                grpc.StatusCode.OUT_OF_RANGE,
                "Fertilizer ratio flow out of range"
            )
        
        device["fertilizer_type"]["fertilizer_ratio"] = request.fertilizer_ratio
        return empty_pb2.Empty()
