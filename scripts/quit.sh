#!/bin/bash

zenity --question --text="Are you sure you want to close?"

[ $? -eq 0 ] && echo 'awesome.quit'
