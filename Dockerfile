FROM alpine:3.9
MAINTAINER Erignoux Laurent <lerignoux@gmail.com>

RUN apk update && apk add --no-cache python3 && \
	rm -rf /var/cache/apk/*

ADD ./* /proxy

WORKDIR /proxy/src

ENTRYPOINT ["python"]
