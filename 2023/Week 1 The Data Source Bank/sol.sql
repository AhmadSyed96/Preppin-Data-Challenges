# Output 1: Total Values of Transactions by each bank
SELECT 
	REGEXP_SUBSTR(Transaction_Code, '[a-z]+') as Bank,
	SUM(Value) as Value
FROM
	PD_2023_Wk_1_Input
GROUP BY
	1;

# Output 2: Total Values by Bank, Day of the Week and Type of Transaction
SELECT 
	REGEXP_SUBSTR(Transaction_Code, '[a-z]+') as Bank,
	CASE WHEN Online_or_In_Person 1 THEN 'Online' ELSE 'In-Person' END AS Online_or_In-Person,
	DAYNAME(Transacion_Date) AS Transacion_Date,
	SUM(Value) as Value
FROM
	PD_2023_Wk_1_Input
GROUP BY
	1, 2, 3;

# Output 3: Total Values by Bank and Customer Code
SELECT 
	REGEXP_SUBSTR(Transaction_Code, '[a-z]+') as Bank,
	Customer_Code,
	SUM(Value) as Value
FROM
	PD_2023_Wk_1_Input
GROUP BY
	1, 2