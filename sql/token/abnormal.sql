SELECT t.[Date and Time]
    , t.[Event message]
    , t.[Description #1]
    , t.[Description #2]
    , t.[Card number]
    , u.[first_name]
    , u.[last_name]
FROM tokens AS t
    LEFT JOIN users AS u ON u.token IN (
        t.[Description #1]
        , t.[Description #2]
    )
WHERE 0 = 0
    -- Exclude administration
    AND t.[Event message] NOT IN (
        'Automatic report requested'
        , 'Server communication failed'
    )
    AND t.[Description #1] NOT IN (
        'Database closed'
        , 'Database open'
        , 'KT-400'
        , 'KT-400 Salle Serveurs'
        , 'Multi-Site Gateway'
        , 'SmartLink'
    )
    AND t.[Description #1] NOT LIKE '%Server Workstation'

    -- Exclude closings
    AND t.[Event message] NOT IN(
        'Door closed/normal condition'
        , 'Door forced open restored'
        , 'In/Out Entry'
        , 'Time-out on access granted'
    )
    AND t.[Description #1] NOT LIKE '% - Exit'

    -- Exclude maintenance
    --AND t.[Description #2] NOT LIKE 'PMT18%'
    --AND t.[Card number] != '0204:02795'
        
    -- Exclude owners
    --AND t.[Description #2] NOT LIKE 'PMT19%'
    --AND t.[Description #2] NOT LIKE 'PMT23%'
    --AND t.[Description #2] NOT LIKE 'PMT24%'
    
    -- Exclude vetted resources
    --AND t.[Description #2] NOT LIKE 'PMT10%'
    --AND t.[Description #2] NOT LIKE 'PMT17%'
    --AND t.[Description #2] NOT LIKE 'PMT20%'
    --AND t.[Description #2] NOT LIKE 'PMT25%'

    -- Exclude working days and hours
    AND (
        STRFTIME('%w', t.[Date and Time]) NOT BETWEEN '1' AND '5' -- 1: Monday - 5: Friday
        OR TIME(t.[Date and Time]) < '07:00:00'  -- First arrival time
        OR TIME(t.[Date and Time]) >= '16:15:00'  -- Shipping closing time
    )

    -- Exclude fake positives
    AND NOT (
        DATE(t.[Date and Time]) = '2026-01-18'
        AND t.[Event message] IN (
            'Pre-alarm door opened too long'
            , 'Door open too long'
        )
    )
    AND NOT (
        DATE(t.[Date and Time]) <= '2026-01-27'
        AND t.[Event message] = 'Door forced open'
    )

ORDER BY t.[Date and Time] ASC
;
