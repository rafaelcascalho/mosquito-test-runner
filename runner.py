import os
import sys

from pathlib import Path
from importlib.util import spec_from_file_location

from runner_exceptions import OutputValidationError, ExceptionValidationError


SUCCESS = '\x1b[92m Passed! \x1b[0m'
FAILED = '\033[91m Failed! \033[0m'
builtins_dict = __builtins__ if type(__builtins__) == dict else __builtins__.__dict__


def handle_assertion(func):
    def assertion_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except OutputValidationError as oe:
            return FAILED, {"expected": oe.expected, "obtained": oe.obtained}
        except ExceptionValidationError as ee:
            return FAILED, ee.message
        else:
            return SUCCESS, None
    return assertion_wrapper


def validate_exception(solution, input):
    try:
        solution(*input)
    except Exception as ex:
        assert ex
        return
    raise ExceptionValidationError("no exceptions were raised")


def validate_output(solution, inputs, output):
    result = solution(*inputs)
    if result != output:
        raise OutputValidationError(expected=output, obtained=result)


def read_tests_and_types(file_path):
    with open(file_path, "r") as file:
        test_cases = file.read().split('\n')[:-1]
    types = test_cases[0].split(',')
    return test_cases[1:], types


def persist_results(results, file_path):
    results_str = '\n'.join(results)
    with open(file_path, "w") as file:
        file.write(results_str)


@handle_assertion
def try_exception_validation(validate_exception, solution, inputs):
    validate_exception(solution, inputs)


@handle_assertion
def try_output_validation(validate_output, solution, inputs, output, types):
    end = len(inputs)
    for index in range(end):
        inputs[index] = builtins_dict[types[index]](
            inputs[index])
    output = builtins_dict[types[-1]](output)
    validate_output(solution, inputs, output)


def import_tests_and_solutions(test_only=""):
    tests_context = []
    challenges_folder_name = "challenges"
    tests_folders = [test_only] if test_only else os.listdir(f'./{challenges_folder_name}')
    for folder in tests_folders:
        base_path = f'{challenges_folder_name}/{folder}'
        test_cases_path = f'./{base_path}/test_cases.txt'
        solution_path = str(Path(__file__).parent / f'{base_path}/solution.py')
        results_path = f'./{base_path}/results.txt'

        tests, types = read_tests_and_types(test_cases_path)
        solution_module = spec_from_file_location("solution", solution_path).loader.load_module()
        solution_function = solution_module.solution

        test_context = {
            'folder_name': folder,
            'solution': solution_function,
            'tests': tests,
            'types': types,
            'results_path': results_path
        }
        tests_context.append(test_context)
    return tests_context


def gen_result_str(base_str, meta_data=""):
    if meta_data:
        return f"{base_str}\n\n{str(meta_data)}\n{'-'*50}"
    return f"{base_str}\n{'-'*50}"


def main(test_only=""):
    results = []
    tests_context = import_tests_and_solutions(test_only=test_only)

    for test_context in tests_context:
        test_cases = test_context['tests']
        types = test_context['types']
        solution = test_context['solution']

        print(f"-> {test_context['folder_name'].capitalize()} tests: \n")
        for case_number, test_case in enumerate(test_cases, start=1):
            values = test_case.split(',')
            inputs, output = values[:-1], values[-1]
            if output == "exception":
                result = try_exception_validation(validate_exception, solution, inputs)
            else:
                result = try_output_validation(validate_output, solution, inputs, output, types)
            result_str = f"Test case number {case_number} result: {result[0]}"
            print(result_str)
            result_str = result_str.replace(SUCCESS, "Passed!")
            result_str = result_str.replace(FAILED, "Failed!")

            full_result = gen_result_str(result_str, result[1]) if result[1] is not None else gen_result_str(result_str)
            results.append(full_result)

        print(f"\n{'=' * 50}")
        persist_results(results, test_context["results_path"])


if __name__ == "__main__":
    cli_args = sys.argv
    if len(cli_args) > 1:
        test_only = sys.argv[1]
        main(test_only)
    else:
        main()
