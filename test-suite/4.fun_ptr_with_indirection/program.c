// Function pointer with indirection
void fun() {}

void id(void (*f)()) {
    f();
}

void f1() {
    id(fun);
}

int main() {
    f1();
    return 0;
}
