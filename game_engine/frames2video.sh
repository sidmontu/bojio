#!/bin/zsh

ffmpeg -f image2 -framerate 25 -pattern_type sequence -start_number 0 -r 0.5 -i out_files/move_%03d.jpg -s 800x800 game.avi
