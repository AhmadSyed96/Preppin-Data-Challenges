
### 2023: Week 1 The Data Source Bank

[January 04, 2023](https://preppindata.blogspot.com/2023/01/2023-week-1-data-source-bank.html "permanent link")

Created by: Carl Allchin

Welcome to a New Year of Preppin' Data. These are weekly exercises to help you learn and develop data preparation skills. We publish the challenges on a Wednesday and share a solution the following Tuesday. You can take the challenges whenever you want and we love to see your solutions. With data preparation, there is never just one way to complete the tasks so sharing your solutions will help others learn too. Share on Twitter, LinkedIn, the Tableau Forums or wherever you want to too. Tag Jenny Martin, Tom Prowse or myself or just use the #PreppinData to share your solutions.

The challenges are designed for learning Tableau Prep but we have a broad community who complete the challenges in R, Python, SQL, DBT, EasyMorph and many other tools. We love seeing people learn new tools so feel free to use whatever tools you want to complete the challenges.

A New Year means we start afresh so January's challenges will be focused on beginners. We will use different techniques each week to help you develop your skills. In February, we will set the challenges at an intermediate level and then in March we will do some advanced challenges. January's challenges will have links to useful videos and blogposts to help you learn a technique if it is new to you.

The subject for January will be our new (fake) bank -- The Data Source Bank (DSB). This week we have had a report with a number of transactions that have not just our transactions but other banks' too. Can you help clean up the data?

### Input

One csv to input this week. You can  [download it here](https://drive.google.com/file/d/1oln2ri6nu1wDQfT3gQMLLNlmQ2h6B9d9/view?usp=share_link).

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgsUOKkk8GcZYYwhHsBtfsNqZc6v2zc0zSnbhAbgfrUF98cdN7ai6ShPZmtJZuRZzio8v2Sovo6QtrzA45eM0Jne3o33sXcE6gmD9qI_j37ABO6eOD7T3cIXQtszMD31hWSNq7AH43Jm5VQdpTOTnfBangz2d_69itGY6ya1qXEPx7d7IWgdleiM_WZSw/w640-h228/Screenshot%202023-01-02%20at%2019.58.57.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgsUOKkk8GcZYYwhHsBtfsNqZc6v2zc0zSnbhAbgfrUF98cdN7ai6ShPZmtJZuRZzio8v2Sovo6QtrzA45eM0Jne3o33sXcE6gmD9qI_j37ABO6eOD7T3cIXQtszMD31hWSNq7AH43Jm5VQdpTOTnfBangz2d_69itGY6ya1qXEPx7d7IWgdleiM_WZSw/s1288/Screenshot%202023-01-02%20at%2019.58.57.png)

  

### Requirements

-   Input the data ([help](https://www.preppindata.com/howto/how-to-connect-to-data-in-files))
-   Split the Transaction Code to extract the letters at the start of the transaction code. These identify the bank who processes the transaction ([help](https://www.preppindata.com/howto/how-to-split-data-fields))

-   Rename the new field with the Bank code 'Bank'.

-   Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values.
-   Change the date to be the day of the week ([help](https://www.preppindata.com/howto/how-to-use-date-functions))
-   Different levels of detail are required in the outputs. You will need to sum up the values of the transactions in three ways ([help](https://www.youtube.com/watch?v=oc7EXJsuDUE&themeRefresh=1)):

-   1. Total Values of Transactions by each bank
-   2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
-   3. Total Values by Bank and Customer Code

-   Output each data file ([help](https://preppindata.blogspot.com/2020/01/how-to-choose-output.html))

### Output

Output 1: Total Values of Transactions by each bank

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicxdE6z3nIP8Cgtdcxwf6lzv73etQh6DFsY18lOvTOCaqDCQofHNjqEFsm1adpIveJa-OeOQ-MgF3l9_7-ge3pNBF8ckzFK30NwL83Yo25hvrQMRMfLqOrLgEU5qTWQpg_Ggq-YYk9o1JM6w14CDVajxkSavF9kRWGNCECbSSXYTs-Sxcz3vxxZ4KlWA/w400-h164/Screenshot%202023-01-02%20at%2020.28.49.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicxdE6z3nIP8Cgtdcxwf6lzv73etQh6DFsY18lOvTOCaqDCQofHNjqEFsm1adpIveJa-OeOQ-MgF3l9_7-ge3pNBF8ckzFK30NwL83Yo25hvrQMRMfLqOrLgEU5qTWQpg_Ggq-YYk9o1JM6w14CDVajxkSavF9kRWGNCECbSSXYTs-Sxcz3vxxZ4KlWA/s400/Screenshot%202023-01-02%20at%2020.28.49.png)

  

Two data fields:

-   Bank
-   Value

3 rows of data (4 including field headers)

  

Output 2: Total Values by Bank, Day of the Week and Type of Transaction

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiHEV1HZBtWSO7VKxq6sQAnZqwv7F8fRDgCrLJSXd-MkvjU5MuDbpSaZjb0hVs8dtocyQysW2VHhCCCisQ0J1lYEyhFJ7yVvQohfU9JAPJpTHyd8J6WK_P3mC-tjPYrJCF1oY1Y2MjOoFaBqJgvwlRSEDqdqk91PGlvQHw3QbcFpZ1arxXkPLOSDOsIsg/w640-h282/Screenshot%202023-01-02%20at%2020.32.11.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiHEV1HZBtWSO7VKxq6sQAnZqwv7F8fRDgCrLJSXd-MkvjU5MuDbpSaZjb0hVs8dtocyQysW2VHhCCCisQ0J1lYEyhFJ7yVvQohfU9JAPJpTHyd8J6WK_P3mC-tjPYrJCF1oY1Y2MjOoFaBqJgvwlRSEDqdqk91PGlvQHw3QbcFpZ1arxXkPLOSDOsIsg/s864/Screenshot%202023-01-02%20at%2020.32.11.png)

  

  

Four data fields:

-   Bank
-   Online or In-Person
-   Transaction Date
-   Value

42 rows of data (43 including field headers)

  

Output 3: Total Values by Bank and Customer Code

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQtzWZh7caA_--D5fbD4CJhm_qRkwdz5SN3DIvMpHfyU6PYQGT9OQcIyBFlNOVOz-CYdQwxIloU6YxCWow9wn7vvULiUX1525i-6jP9pZL8aJbSmerTP3AdW88wUGMoTqFa_P5BG5w3fgak8T3mihPttj2AoETpSFQCIAO9GxFp9tw6zq4RVNsbEmUZQ/s320/Screenshot%202023-01-02%20at%2020.39.27.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQtzWZh7caA_--D5fbD4CJhm_qRkwdz5SN3DIvMpHfyU6PYQGT9OQcIyBFlNOVOz-CYdQwxIloU6YxCWow9wn7vvULiUX1525i-6jP9pZL8aJbSmerTP3AdW88wUGMoTqFa_P5BG5w3fgak8T3mihPttj2AoETpSFQCIAO9GxFp9tw6zq4RVNsbEmUZQ/s602/Screenshot%202023-01-02%20at%2020.39.27.png)

  

Three data fields:

-   Bank
-   Customer Code
-   Value

33 rows of data (34 including field headers)

  

You can download all the  [outputs from here](https://drive.google.com/drive/folders/1-R-TkEc1L14eBv1hPFIWyvb2onReWxg3?usp=share_link)

  

After you finish the challenge make sure to fill in the [participation tracker](https://docs.google.com/forms/d/e/1FAIpQLSdZzudRXwUvjhWwNawwz1kGXcYeQ9gBnAhCOvlA7qEDknGu4A/viewform), then share your solution on Twitter using [#PreppinData](https://twitter.com/search?q=%23preppindata&src=typed_query) and tagging [@Datajedininja](https://twitter.com/Datajedininja), [@JennyMartinDS14](https://twitter.com/JennyMartinDS14) & [@TomProwse1](https://twitter.com/TomProwse1)

You can also post your solution on the [Tableau Forum](https://community.tableau.com/s/group/0F94T000000gQqoSAE/preppindata) where we have a Preppin' Data community page. Post your solutions and ask questions if you need any help!

