connection = "postgresql://postgres:mysecretpassword@localhost:5433/postgres"
task_1_sql = """
SELECT 
	trial_id,
	start_date,
	(
		(SELECT AVG(condition_score)FROM measurements 
		WHERE trial_id = trials.trial_id AND drug != 'Плацебо')
		-
		(SELECT AVG(condition_score)FROM measurements 
		WHERE trial_id = trials.trial_id AND drug = 'Плацебо') 
	) AS difference 	
FROM trials
GROUP BY trial_id, start_date
ORDER BY start_date;"""

task_2_sql = """
SELECT 
	t.trial_id,
	t.start_date,
	t.end_date,
	(
		SELECT condition_score
		FROM measurements m1
		WHERE m1.trial_id = t.trial_id AND m1.drug = 'Плацебо'
		ORDER BY m1.measurement_date DESC
		LIMIT 1 
	) 
	-
	(
		SELECT condition_score
		FROM measurements m2
		WHERE m2.trial_id = t.trial_id AND m2.drug = 'Плацебо'
		ORDER BY m2.measurement_date ASC
		LIMIT 1 
	) AS placebo_score_diff,	

	(
		SELECT condition_score
		FROM measurements m1
		WHERE m1.trial_id = t.trial_id AND m1.drug != 'Плацебо'
		ORDER BY m1.measurement_date DESC
		LIMIT 1 
	)
	-
	(
		SELECT condition_score
		FROM measurements m2
		WHERE m2.trial_id = t.trial_id AND m2.drug != 'Плацебо'
		ORDER BY m2.measurement_date ASC
		LIMIT 1 
	) AS real_drug_score_diff,


	(
		(
			SELECT condition_score
			FROM measurements m1
			WHERE m1.trial_id = t.trial_id AND m1.drug != 'Плацебо'
			ORDER BY m1.measurement_date DESC
			LIMIT 1 
		)
		-
		(
			SELECT condition_score
			FROM measurements m2
			WHERE m2.trial_id = t.trial_id AND m2.drug != 'Плацебо'
			ORDER BY m2.measurement_date ASC
			LIMIT 1 
		)
	) 
	-
	(
		(	
			SELECT condition_score
			FROM measurements m1
			WHERE m1.trial_id = t.trial_id AND m1.drug = 'Плацебо'
			ORDER BY m1.measurement_date DESC
			LIMIT 1 
		)	
		-
		(
			SELECT condition_score
			FROM measurements m2
			WHERE m2.trial_id = t.trial_id AND m2.drug = 'Плацебо'
			ORDER BY m2.measurement_date ASC
			LIMIT 1 
		)
	) AS score_difference
	
FROM trials t 
ORDER BY t.start_date;
 """