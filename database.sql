DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS all_urls;

CREATE TABLE urls (
	id bigint PRIMARY KEY,
	name varchar(255) UNIQUE NOT NULL,
	created_at date NOT NULL
);

CREATE TABLE all_urls (
	id bigint PRIMARY KEY,
	url_name varchar(255) REFERENCES urls(name) NOT NULL,
	check_date date,
	answer int
);
