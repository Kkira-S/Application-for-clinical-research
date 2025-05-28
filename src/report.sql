COPY (
    WITH trial_stats AS (
        SELECT
            t.trial_id,
            t.trial_name,
            COUNT(DISTINCT m.patient_id) AS participants,
            COUNT(DISTINCT CASE WHEN p.gender = 'Male' THEN p.patient_id END) AS males,
            COUNT(DISTINCT CASE WHEN p.gender = 'Female' THEN p.patient_id END) AS females,
            ROUND(AVG(p.age), 1) AS avg_age,
            ROUND(AVG(CASE WHEN m.drug = 'Плацебо' THEN m.condition_score END), 1) AS avg_placebo,
            ROUND(AVG(CASE WHEN m.drug != 'Плацебо' THEN m.condition_score END), 1) AS avg_real_drug
        FROM trials t
        JOIN measurements m ON t.trial_id = m.trial_id
        JOIN patients p ON m.patient_id = p.patient_id
        GROUP BY t.trial_id, t.trial_name
    )
    SELECT
        trial_id,
        participants,
        males,
        females,
        avg_age,
        avg_placebo,
        avg_real_drug,
        trial_name
    FROM trial_stats
    ORDER BY trial_id
) TO '/tmp/trial_statistics.csv' WITH CSV HEADER;
