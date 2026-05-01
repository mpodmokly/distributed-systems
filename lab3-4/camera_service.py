import grpc
from laboratory import camera_pb2, camera_pb2_grpc
from google.protobuf import empty_pb2


class CameraService(camera_pb2_grpc.CameraServiceServicer):
    def __init__(self, database):
        self.db = database

    def GetCameraStatus(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = self.db[device_id]
        return camera_pb2.CameraStatus(
            id=request,
            is_on=device["is_on"],
            pan=device["pan"],
            tilt=device["tilt"],
            zoom=device["zoom"]
        )

    def EnableCamera(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        self.db[device_id]["is_on"] = True
        return empty_pb2.Empty()
    
    def DisableCamera(self, request, context):
        device_id = request.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        self.db[device_id]["is_on"] = False
        return empty_pb2.Empty()

    def SetCameraPan(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")

        if not self.db[device_id]["is_on"]:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Camera must be enabled to set pan")
        
        if request.pan < 0 or request.pan > 359:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, "Pan out of range")

        self.db[device_id]["pan"] = request.pan
        return empty_pb2.Empty()
    
    def SetCameraTilt(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        if not self.db[device_id]["is_on"]:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Camera must be enabled to set tilt")
        
        if request.tilt < 0 or request.tilt > 180:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, "Tilt out of range")
        
        self.db[device_id]["tilt"] = request.tilt
        return empty_pb2.Empty()
    
    def SetCameraZoom(self, request, context):
        device_id = request.id.id
        if not device_id in self.db:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        if not self.db[device_id]["is_on"]:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Camera must be enabled to set zoom")
        
        if request.zoom < 1 or request.zoom > 20:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, "Zoom out of range")
        
        self.db[device_id]["zoom"] = request.zoom
        return empty_pb2.Empty()
