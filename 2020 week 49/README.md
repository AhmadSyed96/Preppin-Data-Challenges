# Preppin' Data 2021 Week 49
<img src='2020 w49.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* nba games

output
* running team ranking

## Briefing & Objective
* create a running ranking of nba teams

## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* create winner
* list home and guest team and explode it
* cumsum wins up to that point
* group by team and game number
* rank

## Problems ran into / What I learned:
* unlike week 3, i found a cleaner way to break the original table into games per team
