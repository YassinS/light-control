#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <token>"
  exit 1
fi

TOKEN=$1

git remote set-url origin https://YassinS:$TOKEN@github.com/YassinS/light-control.git

