package main

import (
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
		url, err := url.Parse(route.Target)
		if err != nil{
			return fmt.Errorf("can't parse url: %w", err)
		}
		// TODO : ReverseProxy 뭔가 URL setting이 문제인듯
		proxies[route.Name] = httputil.NewSingleHostReverseProxy(url)
	}
	return nil
}

func ProxyRequestHandler(proxies Proxies) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request){
		// TODO : Request URL
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
	fmt.Println(proxies)
	r := mux.NewRouter()

	r.HandleFunc("/{param:.*}", ProxyRequestHandler(proxies))

	if err := http.ListenAndServe(":8080", r); err != nil{
		log.Fatal("Server failed.", err)
	}
	
}