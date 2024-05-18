#!/bin/bash

mode=$1
branch_name=$2

if [[ -z "$mode" ]]
then

    echo "mode arg is necessary"
    exit 1

else

    case $mode in
          "persistent")
              docker compose -f docker-compose-persistent.yml up

              exit 0

              ;;
          "start")
              docker build -f Dockerfile -t foodio:latest .

              docker compose -f docker-compose.yml up

              exit 0

              ;;
          "update")
              if [[ -z "$branch_name" ]]
              then

                echo

                echo "invalid Branch name"

                echo

                exit 1

              else

                docker compose -f docker-compose.yml down

                git pull origin "$branch_name" --rebase

                docker build -f Dockerfile -t foodio:latest .

                docker compose -f docker-compose.yml up

                exit 0

              fi
              ;;

          "remove")
              docker compose -f docker-compose.yml down

              exit 0

              ;;

          "clean")
              docker compose -f docker-compose-persistent.yml -f docker-compose.yml down

              exit 0

              ;;

          *)

            echo "Mode is invalid , please try again"
            exit 1
            ;;
      esac

fi
