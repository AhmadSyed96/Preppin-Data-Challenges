### 2023: Week 2 - International Bank Account Numbers

[January 11, 2023](https://preppindata.blogspot.com/2023/01/2023-week-2-international-bank-account.html "permanent link")

Challenge By: Jenny Martin

For week 2 of our beginner month, Data Source Bank has a requirement to construct International Bank Account Numbers (IBANs), even for Transactions taking place in the UK. We have all the information in separate fields, we just need to put it altogether in the following order:

  

[![](https://blogger.googleusercontent.com/img/a/AVvXsEg6cHU6JOCWWyUbCGBixif-Cj3CvRJNRr3RFzcpG7kI8zzL3eAWKBZPdu2UVqivMHILO-zaT2bJ9F2iaNfVWgZIAro_IOwwKi-GjJFVQyJ_O9iE-0X7Iin4vZxbqHiuEsPQp2nDtIjAARQ_aCrSbnmJU6LiU7L64P3gzS68jU9b7_ScOnYI3LOciKGwUw)](https://blogger.googleusercontent.com/img/a/AVvXsEg6cHU6JOCWWyUbCGBixif-Cj3CvRJNRr3RFzcpG7kI8zzL3eAWKBZPdu2UVqivMHILO-zaT2bJ9F2iaNfVWgZIAro_IOwwKi-GjJFVQyJ_O9iE-0X7Iin4vZxbqHiuEsPQp2nDtIjAARQ_aCrSbnmJU6LiU7L64P3gzS68jU9b7_ScOnYI3LOciKGwUw)

  

### Inputs

1.  A list of the transactions, with information about the receiving bank account
    
    [![](https://blogger.googleusercontent.com/img/a/AVvXsEiAItr9blizuA4ej88cecGYqGdUDrReg6X245S-3nwVcwCEdQJTT_Zgq3LaqRPNp3Yk1wDKBarJ2rV-77rWIxmkB9n_d6IH6SniOe-zfAoO0u1iF7_ClvnK_OXoD_yXoshxbhhd633mzwtrYFaTHJu-GbrrBkUeF-meGbHvtIV7wUemkRK-5xO7Djk1qg)](https://blogger.googleusercontent.com/img/a/AVvXsEiAItr9blizuA4ej88cecGYqGdUDrReg6X245S-3nwVcwCEdQJTT_Zgq3LaqRPNp3Yk1wDKBarJ2rV-77rWIxmkB9n_d6IH6SniOe-zfAoO0u1iF7_ClvnK_OXoD_yXoshxbhhd633mzwtrYFaTHJu-GbrrBkUeF-meGbHvtIV7wUemkRK-5xO7Djk1qg)
    
      
    
2.  A lookup table for the SWIFT Bank Codes
    
    [![](https://blogger.googleusercontent.com/img/a/AVvXsEg6fOt52HxeinlLBH6vvkEe80nUpprIXfLmE4H7qwt0U4BNU9n4fzzw-_5bWOI77WJCAId9YFK6Ezzt05F8md6OtyVqeWulnhfukFe1tsv39cQtTU1w952ykX8yb2yOLQp8yyl9ojoj_OHS5vuh6qh61cdI33ZD4ARegghcajZSkj37pErkpnCU_nSHKw)](https://blogger.googleusercontent.com/img/a/AVvXsEg6fOt52HxeinlLBH6vvkEe80nUpprIXfLmE4H7qwt0U4BNU9n4fzzw-_5bWOI77WJCAId9YFK6Ezzt05F8md6OtyVqeWulnhfukFe1tsv39cQtTU1w952ykX8yb2yOLQp8yyl9ojoj_OHS5vuh6qh61cdI33ZD4ARegghcajZSkj37pErkpnCU_nSHKw)
    
      
    

### Requirements

-   [Input the data](https://drive.google.com/drive/folders/10atKDtZtLwyBPOG9NaFiMGzbnZ0jEyCe?usp=share_link)
-   In the Transactions table, there is a Sort Code field which contains dashes. We need to remove these so just have a 6 digit string (_[hint](https://www.youtube.com/watch?v=842bn_H7byU&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=14)_)
-   Use the SWIFT Bank Code lookup table to bring in additional information about the SWIFT code and Check Digits of the receiving bank account (_[hint](https://www.youtube.com/watch?v=UblQU9zVgSk&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=24)_)
-   Add a field for the Country Code (_[hint](https://www.preppindata.com/howto/how-to-create-additional-data)_)

-   Hint: all these transactions take place in the UK so the Country Code should be GB

-   Create the IBAN as above (_[hint](https://www.preppindata.com/howto/how-to-use-string-functions)_)

-   Hint: watch out for trying to combine sting fields with numeric fields - check data types

-   Remove unnecessary fields (_[hint](https://www.youtube.com/watch?v=VIyxvxNtqOI&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=7)_)
-   [Output the data](https://drive.google.com/file/d/1LrzRaNIb25kbgF74x1Si4Bj6a0jsOyMa/view?usp=share_link)

### Output

[![](https://blogger.googleusercontent.com/img/a/AVvXsEgGC22AZ-yZmcUkojCyt9F1d47yJPfgWiVkQCQzLlFsWo9ZxDgZnfjjtuIbxkkvmm4DIlZW2avGb-l5VnMvK59EBLgJ9Fxt54N-GAztcdrlqZzad0aKi6Ipd0uNLPAOcIuNfsXWB8zZ-EmYZN3wswXEG5j11z3hI8yf0v9CYxBR6NE4Xx7nYZixw0AfXg)](https://blogger.googleusercontent.com/img/a/AVvXsEgGC22AZ-yZmcUkojCyt9F1d47yJPfgWiVkQCQzLlFsWo9ZxDgZnfjjtuIbxkkvmm4DIlZW2avGb-l5VnMvK59EBLgJ9Fxt54N-GAztcdrlqZzad0aKi6Ipd0uNLPAOcIuNfsXWB8zZ-EmYZN3wswXEG5j11z3hI8yf0v9CYxBR6NE4Xx7nYZixw0AfXg)

-   2 fields

-   Transaction ID
-   IBAN

-   100 rows (101 including headers)

You can download the [output from here](https://drive.google.com/file/d/1LrzRaNIb25kbgF74x1Si4Bj6a0jsOyMa/view?usp=share_link)

  

After you finish the challenge make sure to fill in the [participation tracker](https://docs.google.com/forms/d/e/1FAIpQLSdZzudRXwUvjhWwNawwz1kGXcYeQ9gBnAhCOvlA7qEDknGu4A/viewform), then share your solution on Twitter using [#PreppinData](https://twitter.com/search?q=%23preppindata&src=typed_query) and tagging [@Datajedininja](https://twitter.com/Datajedininja), [@JennyMartinDS14](https://twitter.com/JennyMartinDS14) & [@TomProwse1](https://twitter.com/TomProwse1)

You can also post your solution on the [Tableau Forum](https://community.tableau.com/s/group/0F94T000000gQqoSAE/preppindata) where we have a Preppin' Data community page. Post your solutions and ask questions if you need any help!
