int *divmod(int a, int b) {
    int *result = new int[2];
    result[0] = a / b;
    result[1] = a % b;
    return result;
}