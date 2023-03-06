from grpc_libs.face_pb2_grpc import AIServiceStub
from grpc_libs.face_pb2 import Request
import grpc
import pickle, time

class PersonGrpcClient:
   
    def __init__(self, ip, port, client_id="app"):

        self.channel = grpc.insecure_channel("{}:{}".format(ip, port))
        self.service_stub = AIServiceStub(self.channel)
        self.client_id = client_id
        print("Connected to GRPC Face Service")

    def detection(self, image):

        image_byte = pickle.dumps([image])
        requests_data = Request(images = image_byte)
        response = self.service_stub.detection_face(requests_data)
        result = pickle.loads(response.results)
        return result
       
    def check_emotion(self, image):

        image_byte = pickle.dumps([image])
        requests_data = Request(images = image_byte)
        response = self.service_stub.check_emotion(requests_data)
        result = pickle.loads(response.results)
        return image_byte
        