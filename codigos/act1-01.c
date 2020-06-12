#include <stdio.h>

/*  Diseñar un programa que ingrese las notas y legajos de un curso por teclado
 utilizando los controles de datos mediante estructuras repetitivas y determine
  cantidad de aprobados reprobados y promocionados imprimir su legajo con una 
  leyenda A o R o P y el operador deberá decidir cuando termina el ingreso de 
  datos ingresando un legajo negativo. Diagrama de flujo y pseudocódigo  */

int main(void)
{
    int alumno_legajo[100];
    float alumno_promedio[100];
    char alumno_estado[100];

    int legajo, nota1, nota2;
    char leyenda;
    int contador = 0; /* número de calificaciones introducidas */

    /* obtiene el primer legajo del alumno */
    printf("Introduzca un legajo, o un numero negativo para terminar (ej: -1): "); /* indicador para la entrada */
    scanf("%d", &legajo);                                                          /* lee el legajo del alumno */

    /* realiza el ciclo mientras no se introduzca el valor negativo */
    while (legajo > 0)
    {
        alumno_legajo[contador] = legajo;
        printf("Introduzca la primera nota: ");
        scanf("%d", &nota1);
        printf("Introduzca la segunda nota: ");
        scanf("%d", &nota2);

        //Calcular el promedio
        alumno_promedio[contador] = (float)(nota1 + nota2) / 2.0;

        //incrementa el contador
        contador = contador + 1;

        /* obtiene el siguiente legajo del alumno */
        printf("Introduzca un legajo, o un numero negativo para terminar (ej: -1): "); /* indicador para la entrada */
        scanf("%d", &legajo);                                                          /* lee el legajo del alumno */
    }

    if (contador != 0)
    {
        for (int i = 0; i < contador; i++)
        {
            if (alumno_promedio[i] < 4)
                leyenda = 'R';
            else if (alumno_promedio[i] < 7)
                leyenda = 'A';
            else
                leyenda = 'P';
            printf("%d%c\n", alumno_legajo[i], leyenda);
        }
    }
    else
    {
        printf("No se introdujo ningun dato valido.\n");
    }
    return 0;
}


/*

INICIO

alumno_legajo[100]
alumno_promedio[100]
alumno_estado[100]
legajo, nota1, nota2
leyenda
contador = 0

Imp("Introduzca un legajo, o un numero negativo para terminar (ej: -1): ")
Leer legajo

Mientras (legajo > 0)
{
    alumno_legajo[contador] = legajo
    Imp("Introduzca la primera nota: ")
    Leer nota1
    Imp("Introduzca la segunda nota: ")
    Leer nota2
    alumno_promedio[contador] = (nota1 + nota2) / 2.0
    contador = contador + 1
    Imp("Introduzca un legajo, o un numero negativo para terminar (ej: -1): ")
    Leer legajo
}

Si (contador != 0)
{
    Para (int i = 0; i < contador; i++)
    {
        Si (alumno_promedio[i] < 4)
            leyenda = 'R'
        Sino Si (alumno_promedio[i] < 7)
            leyenda = 'A'
        Sino
            leyenda = 'P'
        Imp("%d%c", alumno_legajo[i], leyenda)
    }
}
Sino
    Imp("No se introdujo ningun dato valido.")

FIN

*/