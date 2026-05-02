import grpc
from concurrent import futures
from laboratory import common_pb2_grpc
from laboratory import camera_pb2_grpc, irrigation_pb2_grpc, air_conditioner_pb2_grpc
from camera_service import CameraService
from irrigation_service import IrrigationService
from device_registry_service import DeviceRegistryService
from ac_service import ACService
import json
import sys


def serve(config_path, port):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    camera_pb2_grpc.add_CameraServiceServicer_to_server(
        CameraService(config["devices"]),
        server
    )
    irrigation_pb2_grpc.add_IrrigationServiceServicer_to_server(
        IrrigationService(config["devices"]),
        server
    )
    common_pb2_grpc.add_DeviceRegistryServiceServicer_to_server(
        DeviceRegistryService(config["devices"]),
        server
    )
    air_conditioner_pb2_grpc.add_ACServiceServicer_to_server(
        ACService(config["devices"]),
        server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"{config["name"]}")
    print("Server working...")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped")
        server.stop(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Invalid arguments")
    else:
        serve(sys.argv[1], sys.argv[2])
