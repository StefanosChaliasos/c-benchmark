// Simple function pointer call with variable assignment
void fun() {}

int main() {
    void (*fun_ptr)() = &fun;
    void (*fun_ptr2)() = fun_ptr;
    (*fun_ptr2)();
    return 0;
}
