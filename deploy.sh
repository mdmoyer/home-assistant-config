#!/bin/bash

SOURCE=$1

echo Replacing strings
export RAND=`perl -e 'printf("%06d",rand(1000000))'`
find $SOURCE -type f -name "*.yaml" -exec grep QQQ {} \; -exec sed -i "s/QQQ[[:digit:]]\+QQQ/QQQ${RAND}QQQ/g" {} \;
echo Done

rsync -av --exclude="__pycache__" $SOURCE //hassio.local/config/
