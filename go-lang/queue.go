package main

import "fmt"

type Data struct{
	Value string
}

type Queue struct{
	ch chan Data
}

func (q *Queue)Insert(data Data){
	q.ch <- data
}

func (q *Queue)Pop() Data{
	return <- q.ch
}

func queue() {
	q := Queue{make(chan Data)}
	data1 := Data{"Hello"}
	data2 := Data{"World"}

	go q.Insert(data1)
	go q.Insert(data2)

	res := q.Pop()
	fmt.Println(res)
	res = q.Pop()
	fmt.Println(res)
	
}