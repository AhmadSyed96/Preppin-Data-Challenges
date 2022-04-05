# Preppin' Data 2021 Week 39
<img src='2020 w39.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* items and their prices
* customers and what they ordered throughout the week

output
* customer spend at the end of the period and their potential savings

## Briefing & Objective
* the orders and items are structured in an unorthodox manner
* structure the data and aggregate

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* take every other two columns of the prices df and concat to the other repeating columns to get a item, price table
* get per order per personf
* use fuzzymatch to match back on item
* groupby and sum

## What I learned:
* how to use fuzzy matching
