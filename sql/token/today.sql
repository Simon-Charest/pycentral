SELECT t.[Date and Time]
    , t.[Event message]
    , t.[Description #1]
    , t.[Description #2]
    , t.[Card number]
    , u.[first_name]
    , u.[last_name]
FROM tokens AS t
    LEFT JOIN users AS u ON u.token = t.[Description #2]
WHERE 0 = 0
    
    -- Today
    AND DATE(t.[Date and Time]) = DATE('NOW')  
    
    -- Yesterday
    --AND DATE(t.[Date and Time]) = DATE('NOW', '-1 DAY')

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
ORDER BY t.[Date and Time] ASC
;
