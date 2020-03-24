package main

import (
	"google.golang.org/grpc"
	"log"
	"time"
	pb "notifications/proto"
	"context"
	"github.com/golang/protobuf/ptypes"
)

const address = "localhost:50051"

func main() {

	// connection

	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	c := pb.NewNotificationServiceClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()


	notification := &pb.Notification{
		Title:                "test",
		Content:              "xDDD",
		UserId:               "abcdef",
		Time:                 ptypes.TimestampNow(),
	}

	response, err := c.NotificationCreate(ctx, &pb.NotificationCreateRequest{Notification: notification})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	log.Printf(response.Notification.Title)
}
