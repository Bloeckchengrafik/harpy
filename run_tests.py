from rich import console

console = console.Console(
    log_time=True,
    log_path=False,
)

TESTS = [
    "testfiles/type_checker/typechecker_test_basic1",
    "testfiles/type_checker/typechecker_test_basic2",
    "testfiles/type_checker/typechecker_test_basic3",
    "testfiles/type_checker/typechecker_test_basic4",
    "testfiles/type_checker/typechecker_test_variable1",
    "testfiles/type_transformer/tt1",
    "testfiles/compiler/compiler1",
]


def run_tests():
    console.log("[bold green]:sparkles: Running tests...[/bold green]")

    # Run testfiles here
    for test in TESTS:
        try:
            exec(open(f"{test}.py").read())
        except Exception as e:
            console.log(f"[bold red]:x: Test {test} failed with error {e}[/bold red]")
            return
        else:
            console.log(f"[bold green]:white_check_mark: Test {test} passed[/bold green]")

    console.log("[bold green]:tada: All tests passed!")
    exit(0)


if __name__ == '__main__':
    run_tests()

    console.log("[bold red]:x: Some tests failed[/bold red]")
