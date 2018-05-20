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
	num1 float64
	num2 float64
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
	fmt.Println("Please input 1st number: ")
	fmt.Scanln(&num1)
	fmt.Println("Please input 2nd number: ")
	fmt.Scanln(&num2)
	name := defaultName
	if len(os.Args) >1 {
		name = os.Args[1]
	}
	r, err := c.SayHello(context.Background(), &pb.HelloRequest{Name:name,Inputnum1:num1,Inputnum2:num2 })
	if err != nil {
		log.Fatal("could not greet: %v", err)
	}
	log.Printf("Greeting: %s", r.Message)
}