package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"log"
	"net"
	pb "notifications/proto"
	"os"
	"os/signal"
	"time"
	"github.com/golang/protobuf/ptypes"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const port = ":50051"

type NotificationServiceServer struct{}

type NotificationItem struct {
	ID       primitive.ObjectID `bson:"_id,omitempty"`
	Title    string             `bson:"title"`
	Content  string             `bson:"content"`
	UserID	 string             `bson:"user_id"`
	Time	time.Time			`bson:"time"`
}

var db *mongo.Client
var notificationsdb *mongo.Collection
var mongoCtx context.Context

// CREATE

func (s *NotificationServiceServer) NotificationCreate(ctx context.Context, request *pb.NotificationCreateRequest) (*pb.NotificationCreateResponse, error) {
	notification := request.GetNotification()

	// convert proto timestamp to time.Time timestamp
	timestamp, err := ptypes.Timestamp(notification.GetTime())
	if err != nil {
		log.Fatalf("Filed to convert timestamp: %v", err)
	}

	data := NotificationItem{
		//ID:      nil,
		Title:   notification.GetTitle(),
		Content: notification.GetContent(),
		UserID:  notification.GetUserId(),
		Time:    timestamp,
	}


	// Insert the data into the database
	// *InsertOneResult contains the oid
	result, err := notificationsdb.InsertOne(mongoCtx, data)
	// check error
	if err != nil {
		// return internal gRPC error to be handled later
		return nil, status.Errorf(
			codes.Internal,
			fmt.Sprintf("Internal error: %v", err),
		)
	}

	oid := result.InsertedID.(primitive.ObjectID)
	notification.Id = oid.Hex()
	return &pb.NotificationCreateResponse{Notification: notification}, nil
}

// READ

func (s *NotificationServiceServer) NotificationRead(ctx context.Context, request *pb.NotificationReadRequest) (*pb.NotificationReadResponse, error) {

	// mock
	return &pb.NotificationReadResponse{}, nil
}

// UPDATE

func (s *NotificationServiceServer) NotificationUpdate(ctx context.Context, request *pb.NotificationUpdateRequest) (*pb.NotificationUpdateResponse, error) {

	// mock
	return &pb.NotificationUpdateResponse{}, nil
}

// DELETE

func (s *NotificationServiceServer) NotificationDelete(ctx context.Context, request *pb.NotificationDeleteRequest) (*pb.NotificationDeleteResponse, error) {

	// mock
	return &pb.NotificationDeleteResponse{}, nil
}

// LIST

func (s *NotificationServiceServer) NotificationsList(request *pb.NotificationsListRequest, stream pb.NotificationService_NotificationsListServer) error {

	// Initiate a BlogItem type to write decoded data to
	data := &NotificationItem{}
	// collection.Find returns a cursor for our (empty) query
	cursor, err := notificationsdb.Find(context.Background(), bson.M{})
	if err != nil {
		return status.Errorf(codes.Internal, fmt.Sprintf("Unknown internal error: %v", err))
	}
	// An expression with defer will be called at the end of the function
	defer cursor.Close(context.Background())
	// cursor.Next() returns a boolean, if false there are no more items and loop will break
	for cursor.Next(context.Background()) {
		// Decode the data at the current pointer and write it to data
		err := cursor.Decode(data)
		// check error
		if err != nil {
			return status.Errorf(codes.Unavailable, fmt.Sprintf("Could not decode data: %v", err))
		}
		// If no error is found send blog over stream
		stream.Send(&pb.NotificationsListResponse{
			Notification: &pb.Notification{
				Id:       data.ID.Hex(),
				UserId:   data.UserID,
				Content:  data.Content,
				Title:    data.Title,
				//Time:     data.Time,
			},
		})
	}
	// Check if the cursor has any errors
	if err := cursor.Err(); err != nil {
		return status.Errorf(codes.Internal, fmt.Sprintf("Unkown cursor error: %v", err))
	}
	return nil
}

func main() {

	fmt.Println("Starting server on port :50051...")
	listener, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("Failed to listen on port: %v", err)
	}

	// GRPC STUFF

	// slice of gRPC options
	// Here we can configure things like TLS
	opts := []grpc.ServerOption{}
	// var s *grpc.Server
	s := grpc.NewServer(opts...)
	// var srv *BlogServiceServer
	srv := &NotificationServiceServer{}

	pb.RegisterNotificationServiceServer(s, srv)


	// MONGO STUFF

	fmt.Println("Connecting to MongoDB...")
	mongoCtx = context.Background()
	db, err = mongo.Connect(mongoCtx, options.Client().ApplyURI(""))
	if err != nil {
		log.Fatal(err)
	}
	err = db.Ping(mongoCtx, nil)
	if err != nil {
		log.Fatalf("Could not connect to MongoDB: %v\n", err)
	} else {
		fmt.Println("Connected to Mongodb")
	}

	notificationsdb = db.Database("kodesmil_notifications").Collection("notifications")


	go func() {
		if err := s.Serve(listener); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()
	fmt.Println("Server succesfully started on port :50051")


	// STOPPING SERVER

	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt)
	<-c
	fmt.Println("\nStopping the server...")
	s.Stop()
	listener.Close()
	fmt.Println("Closing MongoDB connection")
	db.Disconnect(mongoCtx)
	fmt.Println("Done.")

}
