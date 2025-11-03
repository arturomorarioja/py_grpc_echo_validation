from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import grpc

import echo_pb2 as pb
import echo_pb2_grpc as rpc

class EchoService(rpc.EchoServicer):
    def Say(self, request, context):
        # Validation: text must not be empty or whitespace
        if not request.text or request.text.strip() == '':
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'text must not be empty')

        # If the client did not send a timestamp, fill one
        when = request.when
        if when.seconds == 0 and when.nanos == 0:
            now = datetime.now(timezone.utc)
            when = pb.google_dot_protobuf_dot_timestamp__pb2.Timestamp()
            when.FromDatetime(now)

        print(f"Received: {request.text!r}")

        reply_text = f"You said: {request.text}"
        return pb.Message(text=reply_text, when=when)
    
def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=4))
    rpc.add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Echo server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()