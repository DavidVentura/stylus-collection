#!/bin/sh
for f in *png; do
	convert -quality 80 $f $f.jpg && rm $f;
done
