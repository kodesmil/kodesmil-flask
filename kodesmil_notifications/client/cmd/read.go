package cmd

import (
	"context"
	"fmt"

	pb "notifications/proto"
	"github.com/spf13/cobra"
)

// readCmd represents the read command
var readCmd = &cobra.Command{
	Use:   "read",
	Short: "Find a notification by its ID",
	Long: `Find a notification by it's mongoDB Unique identifier.
	
	If no notification is found for the ID it will return a 'Not Found' error`,
	RunE: func(cmd *cobra.Command, args []string) error {
		id, err := cmd.Flags().GetString("id")
		if err != nil {
			return err
		}
		reqest := &pb.NotificationReadRequest{
			Id: id,
		}
		response, err := client.NotificationRead(context.Background(), reqest)
		if err != nil {
			return err
		}
		fmt.Println(response)
		return nil
	},
}

func init() {
	readCmd.Flags().StringP("id", "i", "", "The id of the blog")
	readCmd.MarkFlagRequired("id")
	rootCmd.AddCommand(readCmd)
}