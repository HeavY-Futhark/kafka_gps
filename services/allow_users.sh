# Change rights in pgsql conf to allow other users to log in

sed -i 's/local   all             postgres                                peer/local   all             postgres                                md5
/' /etc/postgresql/12/main/pg_hba.conf
sudo service postgresql restart
