import grpc
from laboratory import camera_pb2, camera_pb2_grpc


devices = {
    "cam1": {
        "is_on": False,
        "pan": 270,
        "tilt": 90,
        "zoom": 3
    }
}

class CameraService(camera_pb2_grpc.CameraServiceServicer):
    def GetCameraStatus(self, request, context):
        device_id = request.id

        if not device_id in devices:
            context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
        
        device = devices[device_id]
        return camera_pb2.CameraStatus


print(dir(camera_pb2))
