#!/bin/sh
python3 build.py
docker container run -v $(pwd):/slides -it astefanutti/decktape presentation.html presentation.pdf --chrome-arg=--disable-web-security
