package cmd

import (
	"context"
	"fmt"
	"github.com/golang/protobuf/ptypes"
	"time"

	pb "notifications/proto"
	"github.com/spf13/cobra"
)

// updateCmd represents the read command
var updateCmd = &cobra.Command{
	Use:   "update",
	Short: "Find a notification by its ID",
	Long: `Find a notification by it's mongoDB Unique identifier.
	
	If no notification is found for the ID it will return a 'Not Found' error`,
	RunE: func(cmd *cobra.Command, args []string) error {
		// Get the flags from CLI
		id, err := cmd.Flags().GetString("id")
		author, err := cmd.Flags().GetString("author")
		title, err := cmd.Flags().GetString("title")
		content, err := cmd.Flags().GetString("content")
		timestampString, err := cmd.Flags().GetString("time")
		// convert string to Time.time object
		timestampGo, err := time.Parse(time.RFC3339, timestampString)
		// convert Time.time object to Proto format
		timestampProto, err := ptypes.TimestampProto(timestampGo)

		// Create an UpdateBlogRequest
		req := &pb.NotificationUpdateRequest{
			Notification : &pb.Notification{
				Id:       id,
				UserId:   author,
				Title:    title,
				Content:  content,
				Time:     timestampProto,
			},
		}

		res, err := client.NotificationUpdate(context.Background(), req)
		if err != nil {
			return err
		}

		fmt.Println(res)
		return nil
	},
}

func init() {
	updateCmd.Flags().StringP("id", "i", "", "The id of the blog")
	updateCmd.Flags().StringP("user", "u", "", "Add an author")
	updateCmd.Flags().StringP("title", "t", "", "A title for the blog")
	updateCmd.Flags().StringP("content", "c", "", "The content for the blog")
	updateCmd.Flags().StringP("time", "z", "", "The time to notify")
	updateCmd.MarkFlagRequired("id")
	rootCmd.AddCommand(updateCmd)
}
