#include <stdio.h>

/*  
Diseñar un programa que muestre un menú donde se puedan
seleccionar estas distintas opciones y si ingresa otra opción que no sea alguna
de estas mostrar un cartel de error:
1-sumar
2-multiplicar
3-restar
4-dividir
Ejecutar la operación de acuerdo a la opción elegida entre dos números
ingresados por teclado utilizando funciones de entrada y salida de manera adecuada  
*/

int main(void)
{
    int operacion;
    float a, b, resultado;
    printf("Calculadora hecha en C:\n");
    printf("1 - sumar\n");
    printf("2 - multiplicar\n");
    printf("3 - restar\n");
    printf("4 - dividir\n");
    printf("Elija una operacion de la lista de arriba: ");
    scanf("%d", &operacion);

    if (operacion == 1)
    {
        printf("Ingrese los dos numeros a sumar, con un espacio entre el medio.\n");
        scanf("%f %f", &a, &b);
        resultado = (a + b);
    }
    else if (operacion == 2)
    {
        printf("Ingrese los dos numeros a multiplicar, con un espacio entre el medio.\n");
        scanf("%f %f", &a, &b);
        resultado = (a * b);
    }
    else if (operacion == 3)
    {
        printf("Ingrese los dos numeros a restar, con un espacio entre el medio.\n");
        scanf("%f %f", &a, &b);
        resultado = (a - b);
    }
    else if (operacion == 4)
    {
        printf("Ingrese los dos numeros a dividir, con un espacio entre el medio.\n");
        scanf("%f %f", &a, &b);
        resultado = (a / b);
    }
    else
    {
        printf("Error, %d no es una operacion valida.\n", operacion);
        return 1; //retornar error
    }
    
    printf("Resultado de la operacion: %3.5f\n", resultado);
    return 0;
}