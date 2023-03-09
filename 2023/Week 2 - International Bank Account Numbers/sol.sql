SELECT
	'GB' + CAST(Check_Digits AS CHAR) + SWIFT_code + REGEX_REPLACE(Sort_Code, '\-', '') + CAST(Account_Number AS CHAR) AS IBAN
FROM
	Transactions
JOIN
	Swift_Codes USING(Bank)