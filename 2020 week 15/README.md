# Preppin' Data 2021 Week 15
<img src='2020 w15.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* transactions and their items
output
* creating confidence and lift between associated items

## Objective
* derive confidence and lift between associated items

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* explose the transaction items
* self merge on transaction id and take out where the items are the same
* calculate metrics using window functions

## What I learned:
* using nunique with window functions
