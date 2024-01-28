# kafka_gps

## Authors
- Bouchereau Louis,
- Klein Arthur,
- Mosser Hugo.

## Description
Project for the the module "Architectures et Microservices" of ING3 in CY Tech.  
Two producers send gps coordinates to a kafka.  
A consumer gets these coordinates and store them in a database.  
An api access the data of this database.  
A frontend displays the location of the producers on a map.  

## Requirements
- docker 25 or higher,
- at least 8GB of memory available.

## Installation
```bash
git clone https://github.com/HeavY-Futhark/kafka_gps
```

## Lancement
```bash
cd kafka_gps
docker compose up
```
Wait for a log ressembling the following:
```
producer1-1   | INFO:root:Message livré à coordinates [0]
```
Open a browser and go to "localhost:8080".

## Known issues
### Memory
If the program does not run correctly, try running:
```bash
docker compose logs db
```
if the logs indicates no space left on device, the host does not meet the
memory requirements of the project.

### Port disponibility
The project exposes the following ports:
- 9093 for kafka,
- 8080 for the frontend,
- 8000 for the api.
If one of these is used by another program, the creation of the corresponding
container will be impossible.
