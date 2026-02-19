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
ORDER BY t.[Date and Time] ASC
;
