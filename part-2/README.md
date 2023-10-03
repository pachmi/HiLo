# Hi-Lo Game

## What to Do

1. Read the entire README with your partner before doing anything else.
1. With your partner, edit the `hilo.cc` source file using VS Code. Add the required header. Replace all the TODO comments with working code. Remember, make small changes and compile often.
1. Compile your program with the `make` shell command. Use the **debug compile error** procedure to debug any compile errors.
1. Run your program with the `./hilo` shell command.
1. Test that your program passes all of the test cases in the test suite above. If your program suffers a runtime error, use the **debug runtime error** procedure to debug the error. If your program does not produce the expected output, use the **debug logic error** procedure to debug the error.
1. Test your program against automated test with the `$ make test` command. Debug any runtime errors or logic errors using the same procedures.
1. Check your header with the `$ make header` shell command. Correct any errors.
1. Check for format errors with the `$ make format` shell command. Correct any errors.
1. Check for lint errors with the `$ make lint` shell command. Correct any errors.
1. After your program passes all of these tests and checks, push your code to GitHub. Use the usual trio of commands: `git add`, `git commit`, and `git push`.

## Introduction
Finish part 1 before you start part 2.

This program is a first draft of a high/low guessing game. 
The game plays like this:

1. Player one chooses a secret number.
1. Player two guesses the secret number. If they get it right, they win and the game is over.
1. Otherwise (player two guessed wrong), they get a hint that their guess was too high or too low.
1. Player two guesses a second time. If they get it right, they win.
1. Otherwise they lose, and the secret number is revealed.

The game would be more fun if the secret number was hidden or chosen randomly by the computer. We will explore those possibilities in later labs. For now, we are keeping it simple.

In this part, we are not telling you an algorithm to implement. Instead, you and your partner will need to design the program yourselves. You will need to write some `if` statements. This may involve some problem solving and trial error. This kind of practice is exercise that helps you develop as a programmer.

Your program must:
- Print the prompt "Player 1, enter the secret number: ".
- When player two wins, print the message "Correct, you win!".
- When player two guesses too high, print "Too high".
- When player two guesses too low, print "Too low".
- When player two loses, print a message in the form "Incorrect, the secret number was *SECRET-NUMBER*, you lose."

## Building Your Program
To compile your program, you use the `make` command. A Makefile is provided for this exercise.

The Makefile has the following targets:

* all: builds the project
* clean: removes object and dependency files
* spotless: removes everything the clean target removes and all binaries
* format: outputs a [`diff`](https://en.wikipedia.org/wiki/Diff) showing where your formatting differes from the [Google C++ style guide](https://google.github.io/styleguide/cppguide.html)
* lint: output of the [linter](https://en.wikipedia.org/wiki/Lint_(software)) to give you tips on how to improve your code
* header: check to make sure your files have the appropriate header
* test: run tests to help you verify your program is meeting the assignment's requirements. This does not grade your assignment.
* unittest: run unit tests to verify parts of your program performs according to the instructor supplied unit tests.

There are no unittests available for this program.

To test your entire program, use the `make test` command.

## Example Input and Output

Winning on the first guess:
```
$ ./a.out
Player 1, enter the secret number: 6
Player 2, enter your first guess: 6
Correct, you win!
```

Winning after guessing too low:
```
$ ./a.out
Player 1, enter the secret number: 6
Player 2, enter your first guess: 2
Too low
Player 2, enter your second guess: 6
Correct, you win!
```

Winning after guessing too high:
```
$ ./a.out
Player 1, enter the secret number: 6
Player 2, enter your first guess: 8
Too high
Player 2, enter your second guess: 6
Correct, you win!
```

Losing:
```
Player 1, enter the secret number: 6
Player 2, enter your first guess: 1
Too low
Player 2, enter your second guess: 2
Incorrect, the secret number was 6, you lose.
```

## Test Cases

Follow the black box testing procedure to test your program against the test suite below.
(This procedure was described in detail in part 1.)

| Test Case | Input                              | Expected Output              |
|-----------|------------------------------------|------------------------------|
| 1         | secret 5, guess 5                  | ...`win`...                  |
| 2         | secret 5, guess 2, guess 5         | ...`low`...`win`...          |
| 3         | secret 5, guess 8, guess 5         | ...`high`...`win`...         |
| 4         | secret 9, guess 1, guess 3         | ...`low`...`9`...`lose`...   |
| 5         | secret 1, guess 9, guess 6         | ...`high`...`9`...`lose`...  |

## Format Check

Use the command `make format` to check your source code for formatting errors. 

Use the command `make lint` to check your source code for linting errors.

Check to see if your header is correct using the `make header` command.

These formatting and linting requirements are part of the grading rubric.

If you make significant changes to your source file, test it again to confirm that it still passes the test suite. Sometimes a small change that looks benign can actually create a bug.

## Push Your Code

After you have certified that your code passes the test suite and format check, release the code by pushing it to GitHub.

As usualy, you need to
1. Use a computer that is authenticated to git. If your computer is not already authenticated, use the `gcf.sh` script in the **Git Configuration & Authentication* page in Canvas.
1. Add modified file(s) with the `git add` shell command.
1. Create a git commit with the `git commit -m "<MESSAGE>"` shell command.
1. Send the commit to GitHub.com with the `git push` shell command.
1. Refresh the web view of your repo and confirm that your push went through.

If any of these steps trigger an error message, use the **debug command error** flowchart to resolve the problem.

## Next Steps

After you have pushed your code, you are done with this lab. You may ask your TA for permission to sign out and leave.
