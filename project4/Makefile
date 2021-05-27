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

run:
	gcloud compute instances create-with-container \
  		--container-image ghcr.io/elwin/wan:latest \
  		--container-mount-host-path host-path=/home/elwin/c,mount-path=/project4/myself/output/c \
  		--machine-type e2-standard-16 \
  		elwin

destroy:
	gcloud compute instances delete elwin --quiet

copy:
	gcloud compute scp --recurse elwin:/home/elwin/c myself/output