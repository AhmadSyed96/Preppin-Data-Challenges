WITH tragets_pivot AS
	(SELECT Online_or_In_Person, 'Q1' AS Quarter, Q1 AS Quarterly_Targets FROM Quarterly_Targets
	UNION
	SELECT Online_or_In_Person, 'Q2' AS Quarter, Q2 AS Quarterly_Targets FROM Quarterly_Targets
	UNION
	SELECT Online_or_In_Person, 'Q3' AS Quarter, Q3 AS Quarterly_Targets FROM Quarterly_Targets
	UNION
	SELECT Online_or_In_Person, 'Q4' AS Quarter, Q4 AS Quarterly_Targets FROM Quarterly_Targets),
trans_agg AS
	(SELECT
		CASE WHEN Online_or_In_Person = 1 THEN 'Online' ELSE 'In Person' END AS Online_or_In_Person,
		QUARTER(Transaction_Date) AS Quarter,
		SUM(Value) AS Value
	FROM
		Transactions
	GROUP BY
		1,2)
SELECT
	trans_agg.*,
	targets_pivot.Quarterly_Targets,
	trans_agg - targets_pivot.Quarterly_Targets AS Variance_to_Target
FROM
	trans_agg
JOIN
	targets_pivot USING(Online_or_In_Person)