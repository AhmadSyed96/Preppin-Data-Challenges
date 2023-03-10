Challenge by: Jenny Martin

For the third week of beginner month, we're going to be building on the skills that we've already learnt, as well as exploring new concepts. This week may feel a little more challenging, but I promise you're ready for it!

Data Source Bank has some quarterly targets for the value of transactions that are being performed in-person and online. It's our job to compare the transactions to these target figures.

### Inputs

1.  The same transactions file as the first week's
    
    [![](https://blogger.googleusercontent.com/img/a/AVvXsEi5t8Gjk3PuCXgJN9slk6ja37iyookPwAsuBVF3mPTrlH54H4Qpn1a3ailr1sA-Hb0JA8cEyPcZY8MbkflCEq9zPcLmzIimWXKxRuryUdAaqNJRMN3LDfUk5BnvEx-IiIpna4tH2NSZEAduoFhvzZbz9BC3WnGP1uYQx5TpaWUDWjvdkosAEzR017rRqQ=w640-h228)](https://blogger.googleusercontent.com/img/a/AVvXsEi5t8Gjk3PuCXgJN9slk6ja37iyookPwAsuBVF3mPTrlH54H4Qpn1a3ailr1sA-Hb0JA8cEyPcZY8MbkflCEq9zPcLmzIimWXKxRuryUdAaqNJRMN3LDfUk5BnvEx-IiIpna4tH2NSZEAduoFhvzZbz9BC3WnGP1uYQx5TpaWUDWjvdkosAEzR017rRqQ)
    
2.  Quarterly Targets dataset
    
    [![](https://blogger.googleusercontent.com/img/a/AVvXsEhJF9B74360AO-1fdIgkoIPnZU50hlCVfVw03PXf1HDh80iXcBsNZ3h4NGoCq9kJWwyLYKRAh9gK111L5L1T3DJ5zkdrHJM-D9RZBhBoHEVLExm5bizbkLV8qHb-utqUnnjuDox8nJbDIhrVOGWRlsX6InYCLFb5KXdZe6y-apnz8K2qmnDu3_EzI3DDg)](https://blogger.googleusercontent.com/img/a/AVvXsEhJF9B74360AO-1fdIgkoIPnZU50hlCVfVw03PXf1HDh80iXcBsNZ3h4NGoCq9kJWwyLYKRAh9gK111L5L1T3DJ5zkdrHJM-D9RZBhBoHEVLExm5bizbkLV8qHb-utqUnnjuDox8nJbDIhrVOGWRlsX6InYCLFb5KXdZe6y-apnz8K2qmnDu3_EzI3DDg)
    

### Requirements

-   [Input the data](https://drive.google.com/drive/folders/1zbaUf1c_tU1AQBATMB8mMZ28yoyiGRjo?usp=share_link)
-   For the transactions file:

-   Filter the transactions to just look at DSB ([help](https://www.youtube.com/watch?v=1V8c4hOFEUo&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=13))

-   These will be transactions that contain DSB in the Transaction Code field

-   Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
-   Change the date to be the quarter ([help](https://www.preppindata.com/howto/how-to-use-date-functions))
-   Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person) ([help](https://www.youtube.com/watch?v=oc7EXJsuDUE&themeRefresh=1))

-   For the targets file:

-   Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter ([help](https://www.youtube.com/watch?v=yfdNKfuXC-E&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=22))
-   Rename the fields
-   Remove the 'Q' from the quarter field and make the data type numeric (help)

-   Join the two datasets together ([help](https://www.youtube.com/watch?v=UblQU9zVgSk&list=PL_t5OlLHbVGzjl3ygGsOnXbr9sxPOrogY&index=24))

-   You may need more than one join clause!

-   Remove unnecessary fields
-   Calculate the Variance to Target for each row ([help](https://preppindata.blogspot.com/2020/01/how-tomake-calculations.html))
-   Output the data

### Output

[![](https://blogger.googleusercontent.com/img/a/AVvXsEj3vXKjBFRW66fnvwvL44tmvTXdu8C7S_rDUv06WLyM-mIlmh4ZZzbrk9pSGvTx_ZKGkA8_M2s3BtHfIyNAiv7lSq4vecdaLoMqJIcza8kTuMIsdrvQkq7RJ95twwkKjyisa9JlwjsIw_CceE6_7dRIdOkfmRhLSju1eoSFPHpZEuzoM2ohlWvgtA9rsQ)](https://blogger.googleusercontent.com/img/a/AVvXsEj3vXKjBFRW66fnvwvL44tmvTXdu8C7S_rDUv06WLyM-mIlmh4ZZzbrk9pSGvTx_ZKGkA8_M2s3BtHfIyNAiv7lSq4vecdaLoMqJIcza8kTuMIsdrvQkq7RJ95twwkKjyisa9JlwjsIw_CceE6_7dRIdOkfmRhLSju1eoSFPHpZEuzoM2ohlWvgtA9rsQ)

-   5 fields

-   Online or In-Person
-   Quarter
-   Value
-   Quarterly Targets
-   Variance to Target

-   8 rows (9 including headers)

After you finish the challenge make sure to fill in the [participation tracker](https://docs.google.com/forms/d/e/1FAIpQLSdZzudRXwUvjhWwNawwz1kGXcYeQ9gBnAhCOvlA7qEDknGu4A/viewform), then share your solution on Twitter using [#PreppinData](https://twitter.com/search?q=%23preppindata&src=typed_query) and tagging [@Datajedininja](https://twitter.com/Datajedininja), [@JennyMartinDS14](https://twitter.com/JennyMartinDS14) & [@TomProwse1](https://twitter.com/TomProwse1)

You can also post your solution on the [Tableau Forum](https://community.tableau.com/s/group/0F94T000000gQqoSAE/preppindata) where we have a Preppin' Data community page. Post your solutions and ask questions if you need any help!
