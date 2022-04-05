# Preppin' Data 2021 Week 33
<img src='2020 w33.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* daily sales for each scent code
* pricing for each scent(by code and name)
* units ordered

output
* profit rank for each scent

## Briefing & Objective
* this company orders 700 units of each scent weekly thinking it will sell 100 daily; any extras by week end are discarded.
* we are tasked with finding out how much the company loses out on waste through this mode of operation

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* merge df sales on scent code
* create units sold and cogs columns
* group by week of and scent 
* merge df orders by week of order
* create waste cost and profit columns
* groupby scent and profit

## What I learned:
* N/A
