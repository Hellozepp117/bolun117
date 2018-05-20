// server.go
package main
import (
"log"
"net"
"golang.org/x/net/context"
"google.golang.org/grpc"
pb"./hello"
	"strconv"
)

const (
	port = ":50051"
)


type server struct {}

func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "Hello " + in.Name +"\n" + strconv.FormatFloat(in.Inputnum1 , 'E', -1, 64)+ strconv.FormatFloat(in.Inputnum2 , 'E', -1, 64) + "="+ strconv.FormatFloat(in.Inputnum1 + in.Inputnum2 , 'E', -1, 64)}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatal("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	s.Serve(lis)
}