int g;
int my_sn_write(int* p) {
    return 0;
}

struct MYFILE {
    int (*pt) (int* p);
};

struct MyStruct {
    const struct MYFILE *myfile;
};

const struct MYFILE pts = { .pt = my_sn_write };
const struct MyStruct ms = { .myfile = &pts };

void my_vfprintf(const struct MyStruct *ms) {
    int *p = &g;
    ms->myfile->pt(p);
}

int main() {
    my_vfprintf(&ms);
    return 0;
}

