//  Alias due to function pointer resolution.
void f(int *m, int *n)
{}

typedef void (*fp)(int*m, int*n);

int main()
{
	int a,b,c,d;
	int *pa, *pb;
    fp p;
	pa = &a, pb = &b;
	f(pa, pb);
    p = f;
	pb = &a;
    (*p)(pa, pb); 
	return 0;
}

