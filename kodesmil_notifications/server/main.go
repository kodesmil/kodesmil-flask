package main

import (
	"context"
	"google.golang.org/grpc"
	"log"
	"net"
	pb "sample/proto"

)

const port = ":50051"

type sampleService struct{}

func (s *sampleService) Generate(ctx context.Context, in *pb.SampleRequest) (*pb.SampleResponse, error) {
	log.Printf("Received sample %v ", in.Text)
	return &pb.SampleResponse{Id: "kekeke"}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen on port: %v", err)
	}

	server := grpc.NewServer()
	pb.RegisterSampleServiceServer(server, &sampleService{})
	if err := server.Serve(lis); err != nil {
		log.Printf("XD")
	}
}
