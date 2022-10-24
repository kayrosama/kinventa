#!/bin/bash

echo "Borrando base de datos actual"
sudo rm -r /Users/ronin/ksrc/kinventa/db.sqlite3

echo "Restaurando base de datos nueva"
sudo cp /home/tics/jair/factora/app/deploy/data/factora.sqlite3 /Users/ronin/ksrc/kinventa/db.sqlite3

sudo chmod 7777 /Users/ronin/ksrc/kinventa/db.sqlite3

sudo supervisorctl restart heytest

echo "Terminado proceso"
