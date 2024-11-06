package main

import "fmt"

type Pizza struct {
	Name string
	Size string
	Toppings []string
}

func pizzaStyle(p Pizza) string{
	return p.Name + "pizza is a " + p.Size + " pizza with toppings of " + fmt.Sprint(p.Toppings)
}

type Address struct{
	Street string
	City string
}

func (a Address)PrintAddress() string{
	return a.Street + ", " + a.City
}

type Restaurant struct{
	Name string
	Rating int
	PizzaMenu []Pizza
	Address Address // embedded field Composition


}

func restaurantInfo(r Restaurant) string{
	return r.Name + fmt.Sprint(r.Rating) + fmt.Sprint(r.PizzaMenu)
}
func main() {
	myPizza := Pizza{
		Name: "Pepe",
		Size: "Family",
		Toppings: []string{"tomatoes", "basil"},
	}
	fmt.Println(pizzaStyle(myPizza))


	myAddress := Address{
		Street: "Hello",
		City: "World",
	}
	fmt.Println(myAddress.PrintAddress())

	myRestuarant := Restaurant{
		Name: "Tesla",
		Rating: 5,
		PizzaMenu: []Pizza{myPizza},
		Address: myAddress,
	}
	
	fmt.Println(restaurantInfo(myRestuarant))
	fmt.Printf("%T\n", myRestuarant)

	fmt.Println(myRestuarant.Address.PrintAddress())


}