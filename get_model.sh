#!/bin/bash
IMG_NAME=$1

docker build -t $IMG_NAME .
docker run -t $IMG_NAME sleep infinity &
echo "Image running"
sleep 5
C_ID=$(docker ps -q | head -n1 | awk '{print $1;}')
echo $C_ID
docker cp data/01_raw/. $C_ID:/usr/kedro_ml/data/01_raw/
docker exec $C_ID poetry run kedro run -p sub_churn_train_from_raw
docker cp $C_ID:/usr/kedro_ml/data/06_models/sub_churn_model.pkl sub_churn.pkl
docker stop $C_ID
docker rm $C_ID
