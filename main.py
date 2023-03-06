from grpc_libs.ai_service import serve
import argparse

parser = argparse.ArgumentParser(description='Start micro service by GRPC')
parser.add_argument('--workers', type=int, default=1,
                    help='number of workers')
parser.add_argument('--port', type=int, default=51111,
                    help='port')

args = parser.parse_args()
serve(args.workers, args.port)