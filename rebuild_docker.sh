if docker ps | grep -q FCFB-Cyndaquil-Add-Service; then
    echo STOPPING CYNDAQUIL ADD SERVICE..
    docker stop FCFB-Cyndaquil-Add-Service
    echo CYNDAQUIL ADD SERVICE STOPPED!
    echo
    echo REMOVING OLD CYNDAQUIL ADD SERVICE...
    docker remove FCFB-Cyndaquil-Add-Service
    echo OLD CYNDAQUIL ADD SERVICE REMOVED!
    echo
else
    echo CYNDAQUIL ADD SERVICE NOT RUNNING!
    echo
fi
echo BUILDING NEW CYNDAQUIL ADD SERVICE...
docker build -t "fcfb-cyndaquil-add-service:cyndaquil_add.Dockerfile" . -f cyndaquil_add.Dockerfile
echo NEW CYNDAQUIL ADD SERVICE BUILT!
echo
echo STARTING NEW CYNDAQUIL ADD SERVICE...
docker run -d --restart=always --name FCFB-Cyndaquil-Add-Service fcfb-cyndaquil-add-service:cyndaquil_add.Dockerfile
echo NEW CYNDAQUIL ADD SERVICE STARTED!
echo DONE!

if docker ps | grep -q FCFB-Cyndaquil-Update-Service; then
    echo STOPPING CYNDAQUIL UPDATE SERVICE..
    docker stop FCFB-Cyndaquil-Update-Service
    echo CYNDAQUIL ADD SERVICE STOPPED!
    echo
    echo REMOVING OLD CYNDAQUIL UPDATE SERVICE...
    docker remove FCFB-Cyndaquil-Update-Service
    echo OLD CYNDAQUIL UPDATE SERVICE REMOVED!
    echo
else
    echo CYNDAQUIL UPDATE SERVICE NOT RUNNING!
    echo
fi
echo BUILDING NEW CYNDAQUIL UPDATE SERVICE...
docker build -t "fcfb-cyndaquil-update-service:cyndaquil_update.Dockerfile" . -f cyndaquil_update.Dockerfile
echo NEW CYNDAQUIL UPDATE SERVICE BUILT!
echo
echo STARTING NEW CYNDAQUIL UPDATE SERVICE...
docker run -d --restart=always --name FCFB-Cyndaquil-Update-Service fcfb-cyndaquil-update-service:cyndaquil_update.Dockerfile
echo NEW CYNDAQUIL UPDATE SERVICE STARTED!
echo DONE!

if docker ps | grep -q FCFB-Typhlosion-Ongoing-Games-Service; then
    echo STOPPING TYPHLOSION ONGOING GAMES SERVICE..
    docker stop FCFB-Typhlosion-Ongoing-Games-Service
    echo TYPHLOSION ONGOING GAMES SERVICE STOPPED!
    echo
    echo REMOVING OLD TYPHLOSION ONGOING GAMES SERVICE...
    docker remove FCFB-Typhlosion-Ongoing-Games-Service
    echo OLD TYPHLOSION ONGOING GAMES SERVICE REMOVED!
    echo
else
    echo TYPHLOSION ONGOING GAMES SERVICE NOT RUNNING!
    echo
fi
echo BUILDING NEW TYPHLOSION ONGOING GAMES SERVICE...
docker build -t "fcfb-typhlosion-ongoing-games-service:typhlosion_ongoing_games.Dockerfile" . -f typhlosion_ongoing_games.Dockerfile
echo NEW TYPHLOSION ONGOING GAMES SERVICE BUILT!
echo
echo STARTING NEW TYPHLOSION ONGOING GAMES SERVICE...
docker run -d --restart=always --name FCFB-Typhlosion-Ongoing-Games-Service fcfb-typhlosion-ongoing-games-service:typhlosion_ongoing_games.Dockerfile
echo NEW TYPHLOSION ONGOING GAMES SERVICE STARTED!
echo DONE!