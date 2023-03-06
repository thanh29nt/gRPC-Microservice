from grpc_libs.ai_client import PersonGrpcClient
import argparse
import cv2, numpy as np
import time 

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Face Client')
    parser.add_argument('--ip', default="localhost", type = str,
                      help='Ip address of the server')
    parser.add_argument('--port', default = 51111, type = int,
                      help='expose port of gRPC server')
    args = parser.parse_args()
    client = PersonGrpcClient(args.ip, args.port)
    test = cv2.imread("dependencies/9.jpg")
    res1 =  client.detection(test)
    boxes, labels, probs = res1
    # print(boxes)
    t = time.time()
    cnt = 0
    for box in boxes:
        prob = str(res1[2][cnt])
        cv2.rectangle(test, (box[0], box[1]), (box[2], box[3]), (0, 225, 0), 4)
        
        crop_image = test[box[1] : box[3], box[0] : box[2]]
        # cv2.imshow("Crop", crop_image)
        res = client.check_emotion(crop_image)
        d = {0 : 'neutral', 1 : 'happiness', 2:'surprise', 3:'sadness', 4: 'anger', 
                5: 'disgust', 6: 'fear', 7: 'contempt'}
        emo = str("{}".format(cnt + 1)) + ": " + str(d[res[0]])
        print("Face {}".format(cnt + 1), d[res[0]], sep = ": ")
        cv2.putText(test, emo, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 2)
        cnt += 1
    print("Number of faces : {}".format(cnt))
    print(time.time() - t)
    cv2.imshow('img', test)
    # cv2.imshow('img', crop_image)
    cv2.waitKey(0)
   