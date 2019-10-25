docker stop portainer
docker start portainer
docker rm mosquitto
docker run -itd --name="mosquitto" -p 1883:1883 -p 9001:9001 --restart always -v c:/docker/mqtt_broker/mosquitto.conf:/mosquitto/config/mosquitto.conf -v mosquitto_data:/mosquitto/data -v mosquitto_data:/mosquitto/log eclipse-mosquitto
docker rm mc-server
docker run --name mc-server -v c:\docker\mqttcool\my-connector_conf.xml:/mqtt.cool/mqtt_connectors/mqtt_master_connector_conf.xml -d -p 8080:8080 mqttcool/mqtt.cool
cd C:\docker\mqtt_connections
timeout /t 5 /nobreak
docker-compose down
docker-compose up -d
timeout /t 5 /nobreak
cd cd:\docker\tig_stack
docker-compose down
docker-compose up -d