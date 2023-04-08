if docker ps | grep -q FCFB-Cyndaquil-Add; then
    echo STOPPING CYNDAQUIL SERVICE..
    docker stop FCFB-Cyndaquil-Add
    docker stop FCFB-Cyndaquil-Update
    echo CYNDAQUIL SERVICE STOPPED!
    echo
    echo REMOVING OLD CYNDAQUIL SERVICE...
    docker remove FCFB-Cyndaquil-Add
    docker stop FCFB-Cyndaquil-Update
    echo OLD CYNDAQUIL SERVICE REMOVED!
    echo
else
    echo CYNDAQUIL SERVICE NOT RUNNING!
    echo
fi
echo BUILDING NEW CYNDAQUIL SERVICE...
docker build -t "fcfb-cyndaquil-service:Cyndaquil-Add-Dockerfile" .
docker build -t "fcfb-cyndaquil-service:Cyndaquil-Update-Dockerfile" .
echo NEW CYNDAQUIL SERVICE BUILT!
echo
echo STARTING NEW CYNDAQUIL SERVICE...
docker run -d --restart=always --name FCFB-Game-Historian fcfb-game-historian:Cyndaquil-Add-Dockerfile
docker run -d --restart=always --name FCFB-Game-Historian fcfb-game-historian:Cyndaquil-Update-Dockerfile
echo NEW CYNDAQUIL SERVICE STARTED!
echo DONE!