from datetime import datetime, timezone
import grpc

import echo_pb2 as pb
import echo_pb2_grpc as rpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = rpc.EchoStub(channel)

    text = input("Enter a message: ").strip()

    # The request is built with the current timestamp
    msg = pb.Message(text=text)
    msg.when.FromDatetime(datetime.now(timezone.utc))

    try:
        reply = stub.Say(msg, timeout=5.0)
        print("Server replied:", reply.text)
        print("Timestamp roundtrip (UTC):", reply.when.ToDatetime().isoformat())
    except grpc.RpcError as e:
        print(f"gRPC error: code={e.code().name} details={e.details()}")

    channel.close()

if __name__ == "__main__":
    run()