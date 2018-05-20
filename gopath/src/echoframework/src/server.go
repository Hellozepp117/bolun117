
package echo

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc")

type EchoServerImp struct {

}

func (e *EchoServerImp) Echo(ctx context.Context, req *echo.EchoReq) (*echo.EchoRes, error) {
	fmt.Printf("message from client: %v\n", req.GetMsg())

	res := &echo.EchoRes{
		Msg: req.GetMsg(),
	}

	return res, nil
}
