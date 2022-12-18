# Mosquito test runner (WIP)

The simplest, smallest test runner I could thought about building.

## Prerequisites

- Python 3.10.7

## How to run it

1. Clone the repo
2. Create a `test_cases.txt` in the root
3. Run the command below
   ```sh
   $ python runner.py
   ```
4. See the output results in the terminal

## Features

- [ :heavy_check_mark ] Read test cases from txt file
- [ :heavy_check_mark: ] Run validations for results and exceptions
- [ :heavy_check_mark: ] Write results in a txt file
- [ :heavy_multiplication_x: ] Support multiple test using a folder for tests, where test cases, solutions and results are placed together
- [ :heavy_multiplication_x: ] Improve results file structure
- [ :heavy_multiplication_x: ] Write context for failed tests in results file
