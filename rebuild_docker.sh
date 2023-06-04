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
docker run -d --restart=always --name FCFB-Cyndaquil-Add-Service -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-cyndaquil-add-service:cyndaquil_add.Dockerfile
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
docker run -d --restart=always --name FCFB-Cyndaquil-Update-Service -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-cyndaquil-update-service:cyndaquil_update.Dockerfile
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
docker run -d --restart=always --name FCFB-Typhlosion-Ongoing-Games-Service -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-typhlosion-ongoing-games-service:typhlosion_ongoing_games.Dockerfile
echo NEW TYPHLOSION ONGOING GAMES SERVICE STARTED!
echo DONE!

if docker ps | grep -q FCFB-Typhlosion-Historic-Games-Service; then
    echo STOPPING TYPHLOSION HISTORIC GAMES SERVICE..
    docker stop FCFB-Typhlosion-Historic-Games-Service
    echo TYPHLOSION HISTORIC GAMES SERVICE STOPPED!
    echo
    echo REMOVING OLD TYPHLOSION HISTORIC GAMES SERVICE...
    docker remove FCFB-Typhlosion-Historic-Games-Service
    echo OLD TYPHLOSION HISTORIC GAMES SERVICE REMOVED!
    echo
else
    echo TYPHLOSION HISTORIC GAMES SERVICE NOT RUNNING!
    echo
fi
echo BUILDING NEW TYPHLOSION HISTORIC GAMES SERVICE...
docker build -t "fcfb-typhlosion-historic-games-service:typhlosion_historic_games.Dockerfile" . -f typhlosion_historic_games.Dockerfile
echo NEW TYPHLOSION HISTORIC GAMES SERVICE BUILT!
echo
echo STARTING NEW TYPHLOSION HISTORIC GAMES SERVICE...
docker run -d --restart=always --name FCFB-Typhlosion-Historic-Games-Service -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-typhlosion-historic-games-service:typhlosion_historic_games.Dockerfile
echo NEW TYPHLOSION HISTORIC GAMES SERVICE STARTED!
echo DONE!

if docker ps | grep -q FCFB-Porygon-Bot; then
    echo STOPPING PORYGON BOT..
    docker stop FCFB-Porygon-Bot
    echo PORYGON BOT STOPPED!
    echo
    echo REMOVING OLD PORYGON BOT...
    docker remove FCFB-Porygon-Bot
    echo REMOVED OLD PORYGON BOT!
    echo
else
    echo PORYGON BOT NOT RUNNING!
    echo
fi
echo BUILDING NEW PORYGON BOT...
docker build -t "fcfb-porygon-bot:porygon_bot.Dockerfile" . -f porygon_bot.Dockerfile
echo NEW PORYGON BOT BUILT!
echo
echo STARTING NEW PORYGON BOT...
docker run -d --restart=always --name FCFB-Porygon-Bot -v /home/apkick/fcfb_scorebugs/:/project/../fcfb/graphics/scorebugs -v /home/apkick/fcfb_win_probability/:/project/../fcfb/graphics/win_probability fcfb-porygon-bot:porygon_bot.Dockerfile
echo NEW PORYGON BOT STARTED!
echo DONE!