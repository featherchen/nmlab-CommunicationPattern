# nmlab-CommunicationPattern

This is a system with simple fibonacci caculator capability and a logging feature using REST, gRPC, MQTT.

## Clone

```
git clone git@github.com:featherchen/nmlab-CommunicationPattern.git
```

## Set up

```
bash ./setting.sh
cd gRPC-with-protobuf
make
```

## Run servers

#### terminal 1

```
cd mysite
python3 manage.py runserver 0.0.0.0:8000
```

#### terminal 2

```
cd gRPC-with-protobuf
python3 server.py --ip 0.0.0.0 --port 8080
```

## Curl

#### POST to get Fibonacci

```
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/rest/fibonacci/ -d "{\"order\":\"10\"}"
```

#### GET to get History

```
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/rest/logs/
```
