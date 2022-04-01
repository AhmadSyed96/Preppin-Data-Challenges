# Preppin' Data 2021 Week 36
<img src='2020 w36.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* students and their classes
* room capacity and use
* teaching hours needed for age groups
* teacher teaching data

output
* utilization % for each subject

## Briefing & Objective
* teachers are saying they are worked too hard. do we have enough teachers for these subjects?
* create a dataframe stating how utizied each subject is

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* get the hours available each day for each teacher for each class
* count number of students available per age per subject
* get total room capacity per suject
* get hours needed for each age
* merge students to rooms on subject calculate rooms needed
* mere hours needed on age, calculate hours required
* groupby subject aggregate
* merge teacher hours available on subject
* calculate percent utilized

## What I learned:
* how to use ranges
