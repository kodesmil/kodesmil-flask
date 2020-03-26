package main

import (
	"notifications/client/cmd"
)

// example command: go run main.go create -u "Kacpi" -t "Test" -c "lorem ipsum" -z "2020-03-25T23:01:39.413+00:00"

func main() {
	cmd.Execute()
}