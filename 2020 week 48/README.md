# Preppin' Data 2021 Week 48
<img src='2020 w48.jpg?raw=true' alt="Python code for bonus charts">

## Tables
input
* Gate connections to each stand
* gate open times
* stands to flight
* time for each gate to reach the remote stands

output
* flights, times you can rach it from a gate, time needed to get there

## Briefing & Objective
* our airport is using a random number generator to assign gates for flights and manually correcting the errors in real time. this has led to passengers going crazyin order to get to their in time. we are assigned the challenge to find a more logical method of assigning the gates
* here are the requirements:
  * The gate is needed for 45 mins for each flight i.e. a flight which is boarding at 6am will need the gate up to (but not including) 6.45am
  * If there are any flights that are only accessible from 1 gate, these should be assigned first and the gate ith the minimum travel distance should be kept
  * Flights at remote stands should be assigned next, to minimise bus transport times for passengers
  * Remaining flights should assigned to gates with the highest transport times to remote stands, so that if additional flights come in, the gates with lower transport times would be available
  * For any ties that we encounter, lower flight numbers should have priority as these are more important flights for Prep Air



## Python code
<a href="solution.py">
<img src='code snippit.jpg?raw=true' alt="Python code">
</a>

##  Steps
* join all four tables to find possible fight-gate pairing
* impliment the priorities and remove them from the newly card df stated above
* concat and merge the time-to-remote-stands dataframe for those gate that need remote access
![87ef6d33a1adb5137e18a3174afab6c131ec823e_hq](https://user-images.githubusercontent.com/66706924/161397985-f3405c23-395d-4a43-a988-4ec063b1587a.gif)

## Problems ran into / What I learned:
* how to make this problem more pythonic. technically you can have a tie while implementing anyone of the priorities buut the problem and hence the code doesnt address that
* learned how to drop using indexes. i extracted the priority rows from the possibilites tables and used the indecies of the priority table to remove rows from the possibilities table
* had a problem figuring out the leftover flights after all the priorities are implimented. technically that leftover flight can cause a gate conflict with any of the flight-gate relationships made by that point. this is why i added an extra unique relationship column at the end to indicate if that gat was being used at that time for another flight
