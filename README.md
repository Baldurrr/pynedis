# pynedis

# INSTALLATION STEPS
QUICK REQUIREMENTS:
```
Create an account at https://mon-compte-client.enedis.fr/ and enable "Collecte de la consommation horaire"
See you collect point id directly on your linky at home or go at https://mon-compte-client.enedis.fr/
Generate an API token at https://enedisgateway.tech/

#####
apt update && apt upgrade
apt install docker docker-compose wget
apt install python3.6 && apt install python3-pip
```

SQL DB config:
```
mkdir -P enedis-db/sql-DB && cd enedis-db
wget https://raw.githubusercontent.com/Baldurrr/pynedis/main/sql-compose.yml
mv sql-compose.yml docker-compose.yml
(Change sql user / sql password ,and others informations in this docker-compose file)
docker-compose up -d

wget https://raw.githubusercontent.com/Baldurrr/pynedis/main/requirements.txt
pip3 install -r requirements.txt

wget https://raw.githubusercontent.com/Baldurrr/pynedis/main/table_setup.py
chmod +x table_setup.py
python3 table_setup.py

(DB configuration is finished)
```
</br>

PYNEDIS config:
```
mkdir pynedis && cd pynedis
wget https://raw.githubusercontent.com/Baldurrr/pynedis/main/docker-compose.yml
(edit docker-compose file following your personnal informations)
docker-compose up -d
```
