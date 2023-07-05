DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS all_urls;
DROP TABLE IF EXISTS url_checks;


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

CREATE TABLE url_checks (
	id bigint PRIMARY KEY,
	url_id bigint REFERENCES urls(id),
	status_code int,
	h1 varchar(255),
	title varchar(255),
	description text,
	created_at date NOT NULL
);
