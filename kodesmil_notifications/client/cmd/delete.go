package cmd

import (
	"context"
	"fmt"

	pb "notifications/proto"
	"github.com/spf13/cobra"
)

// deleteCmd represents the read command
var deleteCmd = &cobra.Command{
	Use:   "delete",
	Short: "Delete a notification by its ID",
	Long: `Delete a notification by it's mongoDB Unique identifier.
	
	If no notification is found for the ID it will return a 'Not Found' error`,
	RunE: func(cmd *cobra.Command, args []string) error {
		id, err := cmd.Flags().GetString("id")
		if err != nil {
			return err
		}
		req := &pb.NotificationDeleteRequest{
			Id: id,
		}
		// We only return true upon success for other cases an error is thrown
		// We can thus omit the response variable for now and just print something to console
		_, err = client.NotificationDelete(context.Background(), req)
		if err != nil {
			return err
		}
		fmt.Printf("Succesfully deleted the notification with id %s\n", id)
		return nil
	},
}

func init() {
	deleteCmd.Flags().StringP("id", "i", "", "The id of the notification")
	deleteCmd.MarkFlagRequired("id")
	rootCmd.AddCommand(deleteCmd)
}