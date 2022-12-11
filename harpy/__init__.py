from rich import print


def create_error_message(error, filename, line_number, column_number, end_col, source_code):
    """
    Creates an error message for the user to see.
    This looks like this:

    {error} (in file {filename} at line {line_number}, column {column_number}):
        {source_code}
        ^~~~~~~~ (here)
    """

    # Create the error message
    error_message = f"{error} (in file {filename} at line {line_number}, column {column_number}):\n"

    # Add the source code
    error_message += f"{source_code}\n"

    # Add the error indicator
    error_message += " " * column_number + "⇡" + " (here)"

    return error_message


def print_error(error):
    print(f"[bold red]:x: {error}[/bold red]")


def print_warning(warning):
    print(f"[bold yellow]:warning: {warning}[/bold yellow]")
