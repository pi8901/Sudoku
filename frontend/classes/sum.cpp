#include <iostream>

extern "C" {
    __attribute__((visibility("default"))) __attribute__((used))

    int* sum(int* a, int* b) {
        int* res = new int;
        *res = *a + *b;
        return res
    }

    int main() {
        int x = 5;
        int y = 7;

        int* sumPtr = sum(&x, &y);
        std::cout <<sumPtr << std::endl;

        delete sumPtr;

        return 0;
    }
}