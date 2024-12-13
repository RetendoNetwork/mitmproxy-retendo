#! /bin/sh
docker build -t mitmproxy-retendo .
docker run -d -p 8081:8081 mitmproxy-retendo
