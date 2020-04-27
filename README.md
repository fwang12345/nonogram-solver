# Nonogram Solver

Solves a square Nonogram puzzle by converting the puzzle to CNF form and solving using Pycosat

## Inputs

Our nonogram solver is compatible with text files and PNG screenshots from the Nonogram App

### Text File Formatting

Each line represented a row or column pattern and should contain positive integers separated by spaces

For a n by n puzzle, there should be exactly 2n lines, the first n of which represent row patterns and 
the last n representing column patterns

## File Structure

nonogram.ipynb: Contains test results of puzzles of varying sizes

nonogram.py: Interface that allows user to input a puzzle to solve

parse.py: Parses pattern numbers from PNG screenshot

solver.py: Parses pattern numbers from text file and solves puzzle pattern numbers

images: Contains image inputs to solver

puzzles: Contains text inputs to solver

## Dependencies

Google Tesseract OCR: https://pypi.org/project/pytesseract/

The following can be installed using pip:

Pycosat

Tkinter

Pygame

OpenCV

PIL

Pytesseract

## Run and Test
Users will have to change line 5 of parse.py depending on where the OCR is installed

To run, simply run the nonogram.py file

To test, run the cells in nonogram.ipynb
