from grpc_libs.face_pb2 import * 
from grpc_libs import face_pb2_grpc
from concurrent import futures
import pickle, grpc, random
import string
import random
from models.emotion import EmotionInference
from models.utralface import LightWeightDetection

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class AIFaceService(face_pb2_grpc.AIService):

    def __init__(self):
        super(face_pb2_grpc.AIService, self).__init__()

        self.detector = LightWeightDetection.getInstance()
        self.emotion = EmotionInference.getInstance()

    def detection_face(self, request, context):

        """Missing associated documentation comment in .proto file."""
        images = request.images 
        image = pickle.loads(images)[0]
        try:
           boxes, labels, probs = self.detector.predict(image)
           return Response(results = pickle.dumps([boxes, labels, probs]))
        except Exception as e:
            return Response(results = pickle.dumps([-1]))

    def check_emotion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        try:
            image = pickle.loads(request.images)
            emotion = self.emotion.predict(image[0])
            return Response(results = pickle.dumps(emotion))
        except Exception as e:
            return Response(results = pickle.dumps([-1]))

def serve(workers,port):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers = workers))
    face_pb2_grpc.add_AIServiceServicer_to_server(
        AIFaceService(), server
    )
    server.add_insecure_port("0.0.0.0:{}".format(port))
    server.start()
    print("Start done in port: ", port)
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()