echo STOPPING CYNDAQUIL SERVICE..
docker stop FCFB-Cyndaquil-Service
echo CYNDAQUIL SERVICE STOPPED!
echo
echo REMOVING OLD CYNDAQUIL SERVICE...
docker remove FCFB-Cyndaquil-Service
echo OLD CYNDAQUIL SERVICE REMOVED!
echo
echo BUILDING NEW CYNDAQUIL SERVICE...
docker build -t "fcfb-cyndaquil-service:Dockerfile" .
echo NEW CYNDAQUIL SERVICE BUILT!
echo
echo STARTING NEW CYNDAQUIL SERVICE...
docker run -d --restart=always --name FCFB-Cyndaquil-Service fcfb-cyndaquil-service:Dockerfile
echo NEW CYNDAQUIL SERVICE STARTED!
echo DONE!