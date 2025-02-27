# sudo docker build --no-cache -t cjbates02/recon_worker .
sudo docker buildx build --platform linux/amd64 --no-cache -t cjbates02/recon_worker .
sudo docker login --username=cjbates02
sudo docker push cjbates02/recon_worker
sudo docker run -t --network=host cjbates02/recon_worker

