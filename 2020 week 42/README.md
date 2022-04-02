# Preppin' Data 2021 Week 42
<img src='2020 w42.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* daily sales
* quota numbers for income and target

output
* progress to date tracking

## Briefing & Objective
* find how good the company has been in relation to its targets

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* split into yearly and weekly for both the transaction and target tables
* join the tables of the same time frquency
* concat

## Problems ran into / What I learned:
* i was deriving the previous time frames metrics through simply subtracting a year from the current transaction date but found it to be incomprehensive as the most current year ended with a couple of days unaccounted for in the last month. as a result that month for previous years showed incomplete statistics. on top of this any month not shown in the most current year wouldnt show up for previous years
