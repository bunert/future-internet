REGISTRY=ghcr.io/elwin
REPOSITORY=wan
VERSION=latest

clean:
	rm -f myself/output/{a,b,c}/*

build:
	docker build . -t $(REPOSITORY)

publish: build
	docker tag $(REPOSITORY) $(REGISTRY)/$(REPOSITORY):$(VERSION)
	docker push $(REGISTRY)/$(REPOSITORY):$(VERSION)