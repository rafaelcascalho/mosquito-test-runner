from solution import solution


SUCCESS = '\x1b[92m Passed! \x1b[0m'
FAILED = '\033[91m Failed! \033[0m'
builtins_dict = __builtins__ if type(__builtins__) == dict else __builtins__.__dict__


def handle_assertion(should_pass=False):
    def handle_assertion_wrapper(func):
        def assertion_wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                if not should_pass:
                    return SUCCESS
            except AssertionError:
                if should_pass:
                    return SUCCESS
            return FAILED
        return assertion_wrapper
    return handle_assertion_wrapper


def validate_exception(input):
    try:
        solution(*input)
    except Exception as ex:
        assert ex


def validate_output(inputs, output):
    result = solution(*inputs)
    assert result == output


def extract_test_cases():
    with open("test_cases.txt", "r") as file:
        test_cases = file.read().split('\n')[:-1]
    types = test_cases[0].split(',')
    return test_cases[1:], types


def persist_results(results):
    results_str = '\n'.join(results)
    with open("results.txt", "w") as file:
        file.write(results_str)


@handle_assertion(should_pass=True)
def try_exception_validation(validate_exception, inputs):
    validate_exception(inputs)


@handle_assertion()
def try_output_validation(validate_output, inputs, output, types):
    end = len(inputs)
    for index in range(end):
        inputs[index] = builtins_dict[types[index]](
            inputs[index])
    output = builtins_dict[types[-1]](output)
    validate_output(inputs, output)


def main():
    results = []
    test_cases, types = extract_test_cases()

    for case_number, test_case in enumerate(test_cases, start=1):
        passed = SUCCESS
        values = test_case.split(',')
        inputs, output = values[:-1], values[-1]
        if output == "exception":
            passed = try_exception_validation(validate_exception, inputs)
        else:
            passed = try_output_validation(validate_output, inputs, output, types)
        result = f"Test case number {case_number} result: {passed}"
        print(result)
        result = result.replace(SUCCESS, "Passed!")
        result = result.replace(FAILED, "Failed!")
        results.append(result)

    persist_results(results)


if __name__ == "__main__":
    main()
