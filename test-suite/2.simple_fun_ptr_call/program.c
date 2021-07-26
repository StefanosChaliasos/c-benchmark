// Simple function pointer call
void fun() {}

int main() {
    void (*fun_ptr)() = &fun;
    (*fun_ptr)();
    return 0;
}
