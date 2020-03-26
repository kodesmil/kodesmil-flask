package cmd

import (
	"context"
	"fmt"
	"github.com/golang/protobuf/ptypes"

	pb "notifications/proto"
	"github.com/spf13/cobra"
	"time"
)

// createCmd represents the create command
var createCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new notification",
	Long: `Create a new notification on the server through gRPC. 
	
	A blog post requires an AuthorId, Title and Content.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		author, err := cmd.Flags().GetString("user")
		title, err := cmd.Flags().GetString("title")
		content, err := cmd.Flags().GetString("content")
		timestampString, err := cmd.Flags().GetString("time")
		// convert string to Time.time object
		timestampGo, err := time.Parse(time.RFC3339, timestampString)
		// convert Time.time object to Proto format
		timestampProto, err := ptypes.TimestampProto(timestampGo)
		fmt.Print(timestampProto)
		if err != nil {
			return err
		}
		notification := &pb.Notification{
			UserId:  author,
			Title:   title,
			Content: content,
			Time:    timestampProto,
		}
		response, err := client.NotificationCreate(
			context.TODO(),
			&pb.NotificationCreateRequest{
				Notification: notification,
			},
		)
		if err != nil {
			return err
		}
		fmt.Printf("Notification created: %s\n", response.Notification.Id)
		return nil
	},
}

func init() {
	createCmd.Flags().StringP("user", "u", "", "Add an user")
	createCmd.Flags().StringP("title", "t", "", "A title for the notification")
	createCmd.Flags().StringP("content", "c", "", "The content for the notification")
	createCmd.Flags().StringP("time", "z", "", "The time to notify")
	createCmd.MarkFlagRequired("user")
	createCmd.MarkFlagRequired("title")
	createCmd.MarkFlagRequired("content")
	createCmd.MarkFlagRequired("time")
	rootCmd.AddCommand(createCmd)
}
