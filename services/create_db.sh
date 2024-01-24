#! /bin/bash

DB_USER="micro_user"
DB_PWD="password"
DB_NAME="coords"

set -e  # stop immediately on any error

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	CREATE DATABASE IF NOT EXISTS $DB_NAME;
	CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PWD';
	GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

	\c $DB_NAME;
	CREATE TABLE IF NOT EXISTS $DB_NAME (
		id SERIAL PRIMARY KEY,
		ip VARCHAR(15),
		time TIMESTAMP,
		latitude NUMERIC,
		longitude NUMERIC
	);
EOSQL



