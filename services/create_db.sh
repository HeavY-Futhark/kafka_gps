DB_USER="micro_user"
DB_PWD="password"
DB_NAME="coords"

set -e  # stop immediately on any error

#sudo -i -u postgres psql -c "CREATE DATABASE $DB_NAME;"
#sudo -i -u postgres psql -c "CREATE USER $DB_USER with encrypted password '$DB_PWD';"
#sudo psql -U micro_user coords <<EOF
#SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (
#    SELECT FROM pg_database WHERE datname = '$DB_NAME'
#)\gexec
#EOF
#sudo -i -u postgres psql -c "GRANT all privileges on database $DB_NAME TO $DB_USER;"
sudo psql -U micro_user coords <<EOF
CREATE TABLE IF NOT EXISTS $DB_NAME (
	id SERIAL PRIMARY KEY,
    ip VARCHAR(15),
    time TIMESTAMP,
    latitude NUMERIC,
    longitude NUMERIC
);
EOF



