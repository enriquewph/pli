#include <stdio.h>

#define PALABRA "demostracion" 

//esto es un comentario
int main(int argc,char **argv)
{
    printf("Este es un programa de %s en C.\n", PALABRA);
    for (int i = 0; i < 5; i++) /*Comentario*/
        printf("%d\n", i);

    return 0;
}