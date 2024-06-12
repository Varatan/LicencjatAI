SELECT 
    AVG(response_time_seconds) AS average_response_time_seconds
FROM (
    SELECT 
        (strftime('%s', responses.timestamp) - strftime('%s', requests.timestamp)) AS response_time_seconds
    FROM 
        requests 
    JOIN 
        responses 
    ON 
        requests.id = responses.requestID
    GROUP BY responses.requestID
);