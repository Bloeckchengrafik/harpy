#include <cstdio>

const char *
input(const char *prompt) {
    // A Python-like input function.

    // Print the prompt.
    printf("%s", prompt);

    // Read a line of input.
    static char buf[256];
    fgets(buf, sizeof(buf), stdin);

    // Return the input.
    return buf;
}