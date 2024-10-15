#! /bin/sh

docker build . -t ghcr.io/RetendoNetwork/mitmproxy-retendo
docker run -it --rm --name mitmproxy-retendo -v mitmproxy-retendo-data:/home/mitmproxy/.mitmproxy -p 8080:8080 -p 127.0.0.1:8081:8081 ghcr.io/RetendoNetwork/mitmproxy-retendo mitmweb --web-host 0.0.0.0
