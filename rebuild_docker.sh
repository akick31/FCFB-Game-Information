if docker ps | grep -q FCFB-Game-Historian; then
    echo STOPPING GAME HISTORIAN..
    docker stop FCFB-Game-Historian
    echo GAME HISTORIAN STOPPED!
    echo
    echo REMOVING OLD GAME HISTORIAN...
    docker remove FCFB-Game-Historian
    echo OLD GAME HISTORIAN REMOVED!
    echo
else
    echo GAME HISTORIAN NOT RUNNING!
    echo
fi
echo BUILDING NEW GAME HISTORIAN...
docker build -t "fcfb-game-historian:Dockerfile" .
echo NEW GAME HISTORIAN BUILT!
echo
echo STARTING NEW GAME HISTORIAN...
docker run -d --restart=always --name FCFB-Game-Historian fcfb-game-historian:Dockerfile
echo NEW GAME HISTORIAN STARTED!
echo DONE!