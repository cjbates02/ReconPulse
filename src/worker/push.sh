#!/bin/bash

# Build and push the recon worker image
sudo docker build --no-cache -t cjbates02/recon_worker .
sudo docker login --username=cjbates02
sudo docker push cjbates02/recon_worker
# sudo docker run -t --network=host cjbates02/recon_worker

# SSH into the worker nodes and pull down and start the updated image
PURPLE_STACK='10.0.97.212'
RED_STACK='10.0.99.212'
USERNAME='christianbates'

HOSTS=("$PURPLE_STACK" "$RED_STACK")

for HOST in "${HOSTS[@]}"; do
    echo "Updating image on $HOST..."
    ssh "$USERNAME@$HOST" <<EOF
        sudo docker pull cjbates02/recon_worker
        sudo docker stop recon_worker
        sudo docker rm recon_worker
        sudo -E docker run --rm --privileged -e NETWORK="${HOST%.*}.0"/24 -d --network=host --name recon_worker cjbates02/recon_worker
EOF
done








