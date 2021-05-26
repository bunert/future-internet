gcloud compute ssh elwin -- "docker cp \$(docker ps --filter name=elwin -q):/project4/myself/output/c c"
gcloud compute scp --recurse elwin:/home/elwin/c myself/output
