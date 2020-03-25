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
	// convert string id (from proto) to mongoDB ObjectId
	oid, err := primitive.ObjectIDFromHex(request.GetId())
	if err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("Could not convert to ObjectId: %v", err))
	}
	result := notificationsdb.FindOne(ctx, bson.M{"_id": oid})
	// Create an empty BlogItem to write our decode result to
	data := NotificationItem{}
	// decode and write to data
	if err := result.Decode(&data); err != nil {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Could not find blog with Object Id %s: %v", request.GetId(), err))
	}
	var timestamp, err2 = ptypes.TimestampProto(data.Time)
	if err2 != nil {
		log.Fatalf("Error: %v", err2)
	}
	// Cast to ReadBlogRes type
	response := &pb.NotificationReadResponse{
		Notification: &pb.Notification{
			Id:       oid.Hex(),
			UserId:   data.UserID,
			Title:    data.Title,
			Content:  data.Content,
			Time:	  timestamp,
		},
	}
	return response, nil
	// mock
	return &pb.NotificationReadResponse{}, nil
}

// UPDATE

func (s *NotificationServiceServer) NotificationUpdate(ctx context.Context, request *pb.NotificationUpdateRequest) (*pb.NotificationUpdateResponse, error) {
	// Get the notification data from the request
	notification := request.GetNotification()

	// Convert the Id string to a MongoDB ObjectId
	oid, err := primitive.ObjectIDFromHex(notification.GetId())
	if err != nil {
		return nil, status.Errorf(
			codes.InvalidArgument,
			fmt.Sprintf("Could not convert the supplied notification id to a MongoDB ObjectId: %v", err),
		)
	}

	// Convert the data to be updated into an unordered Bson document
	update := bson.M{
		"user_id": notification.GetUserId(),
		"title":      notification.GetTitle(),
		"content":    notification.GetContent(),
		"time":		  notification.GetTime(),
	}

	// Convert the oid into an unordered bson document to search by id
	filter := bson.M{"_id": oid}

	// Result is the BSON encoded result
	// To return the updated document instead of original we have to add options.
	result := notificationsdb.FindOneAndUpdate(ctx, filter, bson.M{"$set": update}, options.FindOneAndUpdate().SetReturnDocument(1))

	// Decode result and write it to 'decoded'
	decoded := NotificationItem{}
	err = result.Decode(&decoded)
	if err != nil {
		return nil, status.Errorf(
			codes.NotFound,
			fmt.Sprintf("Could not find notification with supplied ID: %v", err),
		)
	}

	var timestamp, err2 = ptypes.TimestampProto(decoded.Time)
	if err2 != nil {
		log.Fatalf("Error: %v", err2)
	}

	return &pb.NotificationUpdateResponse{
		Notification: &pb.Notification{
			Id:       decoded.ID.Hex(),
			UserId:   decoded.UserID,
			Title:    decoded.Title,
			Content:  decoded.Content,
			Time:     timestamp,
		},
	}, nil
}

// DELETE

func (s *NotificationServiceServer) NotificationDelete(ctx context.Context, request *pb.NotificationDeleteRequest) (*pb.NotificationDeleteResponse, error) {
	oid, err := primitive.ObjectIDFromHex(request.GetId())
	if err != nil {
		return nil, status.Errorf(codes.InvalidArgument, fmt.Sprintf("Could not convert to ObjectId: %v", err))
	}
	// DeleteOne returns DeleteResult which is a struct containing the amount of deleted docs (in this case only 1 always)
	// So we return a boolean instead
	_, err = notificationsdb.DeleteOne(ctx, bson.M{"_id": oid})
	if err != nil {
		return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Could not find/delete notification with id %s: %v", request.GetId(), err))
	}
	return &pb.NotificationDeleteResponse{
		Success: true,
	}, nil
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

		// decode timestamp
		var timestamp, err2 = ptypes.TimestampProto(data.Time)
		if err2 != nil {
			log.Fatalf("Error: %v", err2)
		}
		// If no error is found send blog over stream
		stream.Send(&pb.NotificationsListResponse{
			Notification: &pb.Notification{
				Id:       data.ID.Hex(),
				UserId:   data.UserID,
				Content:  data.Content,
				Title:    data.Title,
				Time:     timestamp,
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
	db, err = mongo.Connect(mongoCtx, options.Client().ApplyURI("mongodb+srv://kodesmil:SwJ85oNBVNrACZUP@motim0-abanq.mongodb.net/test?authSource=admin&replicaSet=Motim0-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true"))
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