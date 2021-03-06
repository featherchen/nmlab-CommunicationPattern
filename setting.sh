# install dependency
pip3 install -r requirements.txt

# run docker
docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto

# gRPC
sudo apt-get install protobuf-compiler
sudo apt-get install build-essential make
