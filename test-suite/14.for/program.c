// Alias due to context-insensitive
void foo(int *m, int *n)
{}

int main()
{
	int *p, *q;
	int a,b;
    for( a = 10; a < 20; a = a + 1 ){
		p = &a;
		q = &b;
		foo(p,q);
    }
	return 0;
}
