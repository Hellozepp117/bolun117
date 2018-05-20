package main

//client.go

import (
	"log"
	"os"
	"fmt"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	pb"./hello"
)

const (
	address     = "localhost:50051"
)
var (
	defaultName string

)


func main() {
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		log.Fatal("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewGreeterClient(conn)

	fmt.Println("Please input your name: ")
	fmt.Scanln(&defaultName)

	name := defaultName
	if len(os.Args) >1 {
		name = os.Args[1]
	}
	r, err := c.SayHello(context.Background(), &pb.HelloRequest{Name:name})
	if err != nil {
		log.Fatal("could not greet: %v", err)
	}
	log.Printf("Greeting: %s", r.Message)
}