package main

import (
	"context"
	"fmt"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)	
	defer stop() // NotifyContext resource 해제

	fmt.Println("Waiting... Interrupt")

	sig := <- ctx.Done()
	fmt.Println("Received signal.", sig)
	
	// Waiting few seconds for graceful shutdown...
	ctx, cancel := context.WithTimeout(context.Background(), time.Second * 5)
	defer cancel()
	// shutdown services here
	sig = <- ctx.Done()
	fmt.Println("Waiting 5 sec.",sig)
	
}