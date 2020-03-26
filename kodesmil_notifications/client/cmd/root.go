package cmd

import (
	"context"
	"fmt"
	"github.com/mitchellh/go-homedir"
	"log"
	"os"
	"time"

	pb "notifications/proto"
	//homedir "github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"google.golang.org/grpc"
)

var cfgFile string

// Client and context global vars
var client pb.NotificationServiceClient
var requestCtx context.Context
var requestOpts grpc.DialOption

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "notificationsclient",
	Short: "a gRPC client to communicate with the BlogService server",
	Long: `a gRPC client to communicate with the BlogService server.
	You can use this client to create and read blogs.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	//	Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.notificationsclient.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")

	// After Cobra root config init
	// We initialize the client
	fmt.Println("Starting Notifications Service Client")
	// Establish context to timeout if server does not respond
	requestCtx, _ = context.WithTimeout(context.Background(), 10*time.Second)
	// Establish insecure grpc options (no TLS)
	requestOpts = grpc.WithInsecure()
	// Dial the server, returns a client connection
	conn, err := grpc.Dial("localhost:50051", requestOpts)
	if err != nil {
		log.Fatalf("Unable to establish client connection to localhost:50051: %v", err)
	}

	// defer posptones the execution of a function until the surrounding function returns
	// conn.Close() will not be called until the end of main()
	// The arguments are evaluated immeadiatly but not executed
	// defer conn.Close()

	// Instantiate the BlogServiceClient with our client connection to the server
	client = pb.NewNotificationServiceClient(conn)
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
		// Find home directory.
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// Search config in home directory with name ".notificationsclient" (without extension).
		viper.AddConfigPath(home)
		viper.SetConfigName(".notificationsclient")
	}

	viper.AutomaticEnv() // read in environment variables that match

	// If a config file is found, read it in.
	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}
}