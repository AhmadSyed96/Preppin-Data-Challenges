# Preppin' Data 2021 Week 13
<img src='2020 w13.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* each ticket
* SLA agreement times per department
output
* close tickets
* department ranks based on agreement met %
* tickets that can still be closed under SLA

## Objective
* take the tickets and based on the SLA agreement times rank the departments and quantify the two statuses

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* extrac ticket id and dept
* determine if it was a weekday or weekend. tickets closed on the weekend roll it bacl to friday, if opened then then move it to monday
* determine business days of ticket life
* only keep the most current iteration of the ticket
* groupby and aggregate to get the three outputs

## What I learned:
* how to store filters as values for multiple use 
* how to find business days
