#!/bin/bash

git add .
git commit -m "Start random restarts"

for i in {1..5}
do
	python pytorch_MNIST_cDCGAN.py
	git add .
	git commit -m "RR v1 z100 e50 $i"

done

echo Attempting push

git push

echo Done!
