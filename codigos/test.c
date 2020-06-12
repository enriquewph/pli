#include <stdio.h>

int main(void)
{
    char *str = "prueba";
    printf("Esto es un codigo de %s", str);

    for (int i = 0; i < 5; i++)
    {
        printf("Contando... %d", i);
        if (i == 3)
            printf("El numero es %d:", 3)
    }
    
    return 0;
}