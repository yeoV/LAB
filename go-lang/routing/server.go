package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"

	"github.com/gorilla/mux"
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
		proxies[route.Name] = proxy
	}
	return nil
}

func ProxyRequestHandler(proxies Proxies) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request){
		vars := mux.Vars(r)
		serverName := vars["param"]

		server, ok := proxies[serverName]
		if !ok{
			http.Error(w, fmt.Sprintf("Invalid server name: %s", serverName), http.StatusBadRequest)
			return
		}
		// Logging inbound info
		log.Printf("Incoming Request URL: %s, Host: %s\n", r.URL, r.Host)
		server.ServeHTTP(w, r)
		log.Printf("Successfully proxied request to server: %s, Target URL: %s", serverName, r.URL)

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
	r := mux.NewRouter()
	log.Printf("Routing Server Starting . . .")
	r.HandleFunc("/{param:.*}", ProxyRequestHandler(proxies))

	if err := http.ListenAndServe(":8080", r); err != nil{
		log.Fatal("Server failed.", err)
	}
	
}