from harpy.rt.RT import RT


class RTPrint(RT):
    def depends(self) -> list:
        return []

    def cpp(self) -> str:
        return """
#include <iostream>

void print(const char *s) {
    std::cout << s << std::endl;
}  

void print(int i) {
    std::cout << i << std::endl;
}      
"""

    def hpp(self) -> str:
        return """
void print(const char *s);
void print(int i);
"""
