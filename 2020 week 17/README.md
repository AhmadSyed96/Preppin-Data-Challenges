# Preppin' Data 2021 Week 17
<img src='2020 w17.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* answers for each survey response

output
* ranking for each show
* count of devices used

## Objective
* split the table to deal with the other shows column and one for the shows which have their own columns. aggrgate and union

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* rename columns with long names
* melt show columns
* remove dplicates
* create boolean columns for each device
* remove established shows from other shows column
* groupby and aggregate for both outputs

## What I learned:
* how to use pythons built in .join to replace items in a column
