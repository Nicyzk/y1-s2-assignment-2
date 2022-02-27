# Documentation of Code 

## Implementation of find_and_group_matches (used in search_by_keyword and search_by_price)

### The concept of an and_group (with example)  
Note: In a keyword string, AND has precedence over OR.  

Example:  
Let's say we run search_by_keyword and user inputs the keyword string *'Western AND Chicken OR Fries'*.  
For each stall, we want to check if a stall:  
  1. has either a. both keywords 'Western' and 'Chicken' or b. 'Fries'
  2. track if it matches zero keywords, once (a or b) or twice (a and b).

To give precedence for AND over OR, we create a variable called *and_groups*.   
In this case, `and_groups = [ [ 'western', 'chicken' ], [ 'fries' ] ]`. 
We call each nested list an *and_group* as they represent keywords separated by AND.
If the search string has an OR, each group on both sides of the OR e.g. 'Western AND Chicken' and 'Fries',
are created as separate and_groups (nested lists).

### What is and_group_match_count?
Example of structure: 
`and_group_match = 
{
    1: ['stall 1', 'stall 2'],
    2: ['stall 3', 'stall 4']
}`  
Function:
The key represents the number of and_groups matched by all the stalls in the corresponding list (value).

### How and_group_match_count updated (with example)
To create and_group_match_count, we iterate through the keywords of each stall.
Let's say we are at stall 1. If the stall 1's keywords contain all the keywords in the first and_group,
we update a new variable (no_of_and_group_matches) by 1.

After iterating through all and_groups, no_of_and_group_matches is the number of and_groups Stall 1 has matched.

We then update and_group_match_count with Stall 1.
Let's say stall 1 matches 3 and_groups. Then  
`and_group_match_count = {
    3: ['stall 1']
}`

The process is repeated for all the other stalls, until and_group_match_count is filled.



## Implementation of Location-based Search

For each canteen, find *average Euclidean distance* of user 1 and user 2 from canteen.  
`canteen_distance = [['canteen 1', 1], ['canteen 2', 3], ['canteen 3', 2]]`  
After sorted() using *index 1* of inner list, `canteen_distance = [['canteen 1', 1], ['canteen 3', 2], ['canteen 2', 3]]`  
The first k elements are then printed.  
