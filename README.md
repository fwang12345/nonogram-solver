# Nonogram Solver

Solves a square Nonogram puzzle by converting the puzzle to CNF form and solving using Pycosat

## Input File Formatting

Each line represented a row or column pattern and should contain positive integers separated by spaces
For a n by n puzzle, there should be exactly 2n lines, the first n of which represent row patterns and the last n representing column patterns