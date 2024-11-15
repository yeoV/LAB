package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"gopkg.in/yaml.v3"
)

type Config struct{
	Gateway	 GatewayConfig `yaml:"gateway"`
}

type GatewayConfig struct{
	ListenAddr	string `yaml:"listenAddr"`
	Routes 		[]Route `yaml:"routes"`
}

type Route struct{
	Name 	 string `yaml:"name"`
	Context	 string `yaml:"context"`
	Target	 string `yaml:"target"`

}

// Load config file from local to struct object
func LoadConfig(configPath string, config *Config) error{
	content, err := os.ReadFile(configPath)
	if err != nil{
		return fmt.Errorf("can't load config file: %w", err)
	}

	if err := yaml.Unmarshal(content, config); err != nil{
		return fmt.Errorf("invalid config key or values: %w", err)
	}
	return nil
}

// Loaded backend urls convert to reverseproxy url
func CreateReverseProxy(config *Config, proxies Proxies) error{
	for _, route := range config.Gateway.Routes{
		target, err := url.Parse(route.Target)
		if err != nil{
			return errors.New("can't parse url")
		}
		// https://pkg.go.dev/net/http/httputil#NewSingleHostReverseProxy
		proxy := &httputil.ReverseProxy{
			Rewrite: func(pr *httputil.ProxyRequest) {
				pr.SetURL(target)
				pr.Out.URL.Path = route.Context
				pr.SetXForwarded()
				
				// Logging outbound info
				log.Printf("Outbound URL: %s, Host: %s\n", pr.Out.URL, pr.Out.Host)
			},
		}

		// proxy error handler
		proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, err error) {
				log.Printf("Proxy error : %v", err)
				http.Error(w, fmt.Sprintln("Can't connect server."), http.StatusBadGateway)
		}
		proxies[route.Name] = proxy
	}
	return nil
}

func ProxyRequestHandler(proxies Proxies) echo.HandlerFunc{
	return func(c echo.Context) error {
		serverName := c.Param("param")
		proxy, ok := proxies[serverName]
		if !ok{
			return echo.NewHTTPError(http.StatusBadRequest, fmt.Sprintf("invalid server name (URL param). %s", serverName))
		}
		log.Printf("Incoming Request URL: %s\n", c.Request().RequestURI)

		proxy.ServeHTTP(c.Response(), c.Request())
		
		
		log.Printf("Successfully proxied request to server: %s, Target URL: %s", serverName, c.Request().URL)


		return nil
	}
}

type Proxies map[string]*httputil.ReverseProxy
func main() {
	var config Config
	
	proxies := Proxies{}
	configPath := "./config.yaml"
	if err := LoadConfig(configPath, &config); err != nil{
		log.Fatal(err)
	}

	if err := CreateReverseProxy(&config, proxies); err != nil{
		log.Fatal(err)
	}
	
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/:param", ProxyRequestHandler(proxies))

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	// Start
	go func(){
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed{
			e.Logger.Fatal("shutting down the server ")
		}
	}()
	// graceful shutdown

	<-ctx.Done()
	e.Logger.Info("Shutdown signal received")
	
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5* time.Second)
	defer cancel()
	if err := e.Shutdown(shutdownCtx); err != nil{
		e.Logger.Fatal("Failed to gracefully shutdown")
	}
	e.Logger.Info("Server gracefully stopped")
	
}