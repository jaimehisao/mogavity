Listing of Tests 


test9 - Tests the function calling ability of the language, specifically, the scope keeping of the language.
The tests prints values stored in global memory, then calls the function with the same code inside, and prints
different values, then goes back to main and prints the original global value.

The test prints:
"Should output 1"
1 
"Should output 2"
2
"Should output 3"
3
"Should output 1"
1

1 being the global scope, 2 being local and 3 being local2
