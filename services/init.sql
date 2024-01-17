CREATE DATABASE coords;
\c coords;
CREATE USER micro_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE coords TO micro_user;

CREATE TABLE coord (
	id SERIAL PRIMARY KEY,
	ip VARCHAR(15),
	time TIMESTAMP,
	latitude NUMERIC,
	longitude NUMERIC
);
