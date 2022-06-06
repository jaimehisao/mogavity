# Mogavity Compiler Quick Reference

Using the Mogavity compiler is simple. Below you will find simple commands and statements that you can use to implement your code.

Programs done with Mogavity use the **.mog** extension.

Here is a simple Mogavity program.
```
program test;

var int a, b, c, d;

instr void local()
{
    var int a, b, c;
    a = a + 2;
    b = 1 + 6;
    c = a + b;
    return c;
}

main {
    d = _local();
    output -> d;
    return 0;
}
``` 
Lets go over the basics

- Each Mogavity program has a name, in this case **test**, this name goes at the top, accompanied by the word **program**;
- All statements end with a **semicolon** **;**
- Variables can only be declared in the top-level of a scope. Be it global or local.
- To call a function or method, it is needed to put an underscore **_** before the call.
- Our supported types are **ints** and **floats**, both in atomic form or in arrays.
- To print to the screen you use the **output** command, and to recieve data from the user, you use the **input** command. Do note that you need to use an arrow to signify the direction of data. ```input <- X;  output-> X;```
- Creating a function requires the **instr** command beforehand, and it can be a **void**, **int** or **float** function.


## Arrays
Declaring arrays is simple in Mogavity, take a look at the example below.
```
program test;

var int A[5];
var int B[5][5];

main {
    A[2] = 7;
    A[3] = 5;
    output -> A[2];
    output -> A[3];
    A[1] = A[2] * A[3];
    output -> A[1];
    return 0;
}
```
An array is declared by **arrayName[Length]**, and accessed in the same way using an index based of zero. So if you were to access the box 3, you would do **arrayName[2]**.
You can do operations on arrays and matrices just as you would with any other variable. Though they are not supported as parameters in functions.

## Function Calls
Calling a function in Mogavity is simple. 
```
program test;

var int d;

instr int local(int num)
{
    var int a;
    a = num + 2;
    return a;
}

main {
    d = _local();
    output -> d;
    return 0;
}
```
Functions are declared using the **instr** command, followed by the return type and then the function name. 
Inside the parenthesis, parameters can be added by declaring the type and the parameter name. A function can have
more than one parameter and can also have more than one return inside it. Variables instantiated inside a Function
will only be available inside that particular scope.

## Conditionals and Loops
```
program test;

var int a, b, c, d;

main {
    
    a = 1;
    b = 2;
    c = 3;
    d = 4;

    if ((a > b or c < d) and (c < d and a < d)) {
        output -> "negro";
    }
    otherwise {
        output -> "blanco";
    }
}
```
Conditional operators are similar to other programming languanges, we use the standard operators **<**, **>**,
**or** and, **and** which can be used together as seen above. 

The IF statement evaluates boolean operations and executes accordingly (yes or no). If you want to have an "else"
condition, in Mogavity you state it as **otherwise**.

## Object Creation
```
program test;

var int a, b, c, d;

main {
    
    a = 1;
    b = 2;
    c = 3;
    d = 4;

    if ((a > b or c < d) and (c < d and a < d)) {
        output -> "negro";
    }
    otherwise {
        output -> "blanco";
    }
}
```
Mogavity supports user-created objects, they behave a lot like structs from other languages. But they can also have
their own functions.

Conditional operators are similar to other programming languanges, we use the standard operators **<**, **>**,
**or** and, **and** which can be used together as seen above. 

The IF statement evaluates boolean operations and executes accordingly (yes or no). If you want to have an "else"
condition, in Mogavity you state it as **otherwise**.

## TL;DR
- Supported simple types **int**, and **float**. We also support objects of the user's creation.

