package main

import (
	"errors"
	"fmt"
)


var ErrStackIsEmpty = errors.New("stack is empty")
// any -> interface{}
type Stack struct{
	items []any
}

func NewStack() *Stack{
	return &Stack{
		items: make([]any, 0),
	}
}

func (s *Stack)Push(item any){
	s.items = append(s.items, item)
}

func (s *Stack)Pop() (any, error){
	if s.IsEmpty(){
		return nil, ErrStackIsEmpty
	}
	
	lastIndex := len(s.items) - 1
	item := s.items[lastIndex]
	s.items = s.items[:lastIndex]
	return item, nil
	
}

func (s Stack)Peak() (any, error){
	if s.IsEmpty(){
		return nil, ErrStackIsEmpty
	}
	return s.items[len(s.items) - 1], nil

}

func (s Stack)IsEmpty() bool{
	return len(s.items) == 0
}

func (s Stack)Size() int{
	return len(s.items)
}


func stack() {
	stack := NewStack()	
	
	stack.Push("Hello")
	stack.Push("World")
	stack.Push("Golang")

	fmt.Println(stack)
	
	fmt.Printf("Size : %d\n", stack.Size())

	if val, err := stack.Peak(); err == nil{
		fmt.Printf("Peak : %v\n", val)
	}

	res, err := stack.Pop()
	if err == nil{
		fmt.Println(res)
	}

	res2, err := stack.Pop()
	if err == nil{
		fmt.Println(res2)
	}
	fmt.Println(stack)
}