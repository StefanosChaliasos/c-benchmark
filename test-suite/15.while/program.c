// Alias due to context-insensitive
void foo(int *m, int *n)
{}

int main()
{
	int *p, *q;
    int a = 10;
	int b;
    while( a < 20 ) {
		p = &a;
		q = &b;
		foo(p,q);
        a++;
    }
	return 0;
}
