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
    , u.name
    , a.event
FROM alarm AS a
    LEFT JOIN users AS u ON u.id = pr
WHERE DATE(a.datetime) BETWEEN '2026-01-23' AND '2026-01-25'
ORDER BY a.datetime ASC
;
