from laboratory import air_conditioner_pb2, air_conditioner_pb2_grpc


class ACService(air_conditioner_pb2_grpc.ACServiceServicer):
    def __init__(self, database):
        self.db = database
        self.IRRIGATION = "AC"
    