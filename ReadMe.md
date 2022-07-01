# Apes Among Programmers (AAP)
Who doesn't like a cute monkey or ape from time to time? Nobody likes it when they are your colleague's and totally mess up the entire codebase! This language allows you to spend time thinking about apes whilest getting to undestand your colleague's a bit more by getting inside their head. (Yes.. This also means that you need to read the code as if you're an Ape to get the best experience possible.)

Your written AAP code can both be interpreted aswell as be compiled onto a micro controller.
There is currently only support for microcontrollers which make use of the cortex-m0. It works perfectly fine on an Arduino Due for example.

# Turing complete
The AAP language is turing complete! A language is turing complete when it contains conditional branching, when it can change an arbitrary amount of memory and when it's able to use infinite memory. The AAP language suffices on all three of these points which makes it turing complete.
| Requirement | Example |
| ----------- | ------- |
| Conditional branching. | AAP contains If statements. |
| Change an amount of memory. | AAP contains variables. |
| Use infinite memory. | AAP does not limit the memory usage. |

# Functional programming
The codebase is written in a functional manner with Python. There is however simple exception handling to make it a bit easier to figure out what you've done wrong when it doesn't want to interpret or compile your code.

This also means that the python code doesn't make use of any for nor while loops. Just like most of the code has been written recursively. 
### Decorator
There is one existing decorator inside of the codebase: The 'SkipDecorator'. It is located in [parser.py](Interpreter/parser.py) on line 10. This decorator is used to skip over a given Token. This makes it easier to skip over certain tokens until they have passed.

### Typing
The codebase also contains typing. This makes it much easier to see what's going in and out of a function, especially in a language such as Python. I have also included the Haskell notation notation of each function in the Docstrings of the functions.

### Higher order functions
I have made use of multiple higher order functions inside of this codebase. They are obviously a nice to have but in this case they were mandatory. I have used the following higher order functions:
| Function | What does it do | Where |
| -------- | --------------- | ----- |
| <b>map</b> | Append argument to list. | [compiler.py](Compiler/compiler.py) on line 254. |
| <b>zip</b> | Combines the passed arguments with the 'abstract' arguments of a function. | [function.py](Compiler/function.py) on line 38.  |
| <b>reduce</b> | Checks whether there are any nodes which need to return. | [compiler.py](Compiler/compiler.py) on line 158. |
| <b>filter</b> | Removes all None elements from list. | [compiler.py](Compiler/compiler.py) on line 176. |

# Functionality
The AAP language allows the user to make use of <b>While loops</b>. Let your inner gorilla out and start spinning around like they love to do. While loops are however only allowed inside of functions, be aware of this!
```
Wife spinWideRound OpenBanane i CloseBanane
    Ape result Is 0
    SpinWhile i < 5 Then
        Ape result Is i + 1 
        Ape i Is i + 1 StopSpinning 
    Throw result StopWife

Run spinWideRound OpenBanane 0 CloseBanane
```
```
Returns: [5]
```

### Functions
As you may have noticed in the code snipper above: there is more than a while loop.
You can also write functions with AAP. Apes are fond of their wifes so they name their functions accordingly (so romantic). 

#### <b>Stop wife</b>
After you have finished declaring your function, don't forget to stop your wife!! The terminal doesn't like it when there aren't equal rights so don't make your wife's do too much work and be sure to stop them.

### Variables
You can also see that there is mentioning of other Apes. The other apes are variables which you can control and manipulate like a true Alpha Ape.

### Conditional branching
As stated before, the AAP language allows the user to play with conditional branching. They are rather easy to use and they support a new line after the 'Then' Keyword. If you do so however, you are required to stop the statement by placing 'StopIf' after the end of the statement. This can either be with or without an else case. They StopIf always needs to be placed after the 'Else' Keyword however.

The following is allowd for conditional branching
```
If 1 == 1 Then 2

If 1 == 1 Then 2 Else 3

If 1 == 1 Then
    2 Else 
        3 StopIf
```
```
Returns: [2, 2, 2]
``` 
# Syntax
There are a few things to keep in mind while writing code like a monke. This is what you need to pay attention to:

### Statements
There can be multiple functions inside of a file which will be interpreted. This is however not supported by the AAP compiler. If you wish to compile the code: Only one function defenition per file is supported.
### Spaces
Everything needs to be seperated by a space. The code file splits on spaces, so they are truly important. The terminal will surely let you know when you forgot a space, so there is nothing to really worry about.

### New line
Functions defenitions require to be followed by a new line as shown in the code snippet at the While Loop section. 

# Return
Something which is AAP specific is the way the output is given. The final return is in fact a list containing all results from the written code. You may have noticed this already since the output of the code snippets have been underneat the snippets themself. It's not very hard to work with but it is important.

# Running the interpreter
It is fairly easy to run your code with the interpreter! The only thing you have to do is run main.py whilest in the AAP directory and give your .AAP filename as a second parameter. This will interpret your code file and show the result in the terminal.
```
C:/AAP> python main.py main.AAP
```

# Running the compiler
Compiling the code takes a bit more effort before you can start. You are currently required to install gcc and need the library [HWLIB](github.com/wovo/hwlib). 
Set the correct port of your microcontroller in the makefile and then you're ready to go!
Running it is similar to the interpreter. You need to give one more argument however: the output file.
There will automatically be a terminal opened, which shows you the ouput of your code, when you have compiled and flashed the code to your microprocessor.
```
C:/AAP> python main.py main.AAP banane.asm
```