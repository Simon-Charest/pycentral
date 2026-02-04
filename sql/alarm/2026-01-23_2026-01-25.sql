SELECT a.datetime
    , CASE strftime('%w', datetime)
        WHEN '0' THEN 'Dimanche'
        WHEN '1' THEN 'Lundi'
        WHEN '2' THEN 'Mardi'
        WHEN '3' THEN 'Mercredi'
        WHEN '4' THEN 'Jeudi'
        WHEN '5' THEN 'Vendredi'
        WHEN '6' THEN 'Samedi'
    END AS weekday
    , CASE 
        WHEN INSTR(a.event, 'PR:') > 0 THEN
            SUBSTR(
                a.event,
                INSTR(a.event, 'PR:') + 3,
                INSTR(SUBSTR(a.event, INSTR(a.event, 'PR:') + 3), ' ') - 1
            )
        ELSE NULL
    END AS pr
    , u.first_name
    , u.last_name
    , a.event
FROM alarms AS a
    LEFT JOIN users AS u ON u.id = pr
WHERE 0 = 0
    -- Exclude administration
    AND a.event NOT LIKE '%SIGNAL TRAITER%'

    -- Exclude closings
    --AND a.event NOT LIKE 'FERMETURE%'
    
    -- Exclude maintenance
    --AND pr NOT IN ('001', '015')

    -- Exclude owners
    --AND pr NOT IN ('000', '002')

    -- Exclude vetted resources
    --AND pr NOT IN ('016', '017')
    
    -- Exclude tests
    AND a.event != 'TEST CODE GSM/IP'

    AND DATE(a.datetime) >= '2026-01-23'
    AND DATE(a.datetime) <= '2026-01-25'
ORDER BY a.datetime ASC
;
