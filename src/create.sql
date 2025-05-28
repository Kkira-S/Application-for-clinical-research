CREATE TABLE patients (
	patient_id  INTEGER PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	age INTEGER NOT NULL,
	gender VARCHAR(10) NOT NULL,
	condition VARCHAR(100) NOT NULL
);

CREATE TABLE trials (
	trial_id INTEGER PRIMARY KEY,
	trial_name VARCHAR(100) NOT NULL,
	start_date DATE NOT NULL,
	end_date DATE NOT NUll
);

CREATE TABLE measurements (
	measurement_id INTEGER  PRIMARY KEY,
	patient_id INTEGER,
	trial_id INTEGER,
	measurement_date DATE NOT NULL,
	drug VARCHAR(100) NOT NULL,
	condition_score INTEGER,

	CONSTRAINT patient_id_fk FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
	CONSTRAINT trial_id_fk FOREIGN KEY (trial_id) REFERENCES trials (trial_id)
);