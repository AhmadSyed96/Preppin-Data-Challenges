# Preppin' Data 2021 Week 26
<img src='2020 w26.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* internal product id's with sales
* 3rd party product id's with sales

output
* joined table indicated how the  product id's were matched up

## Objective
* join the two tables based on matching ids. for the remaining internals ids match them up based on scent and keep whichever 3rd party id you get with the smallest sales difference; should multiple internal ids return the same 3rd party id during this step, keep the internal id with the lowest sales difference and discard the other(s).

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* match on id
* take out those ids from both internal andd 3rd party
* match on scent
* takes those ids out again 
* concat back

## What I learned:
* mental gymnastics 
