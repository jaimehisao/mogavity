[![Compiler Unit Testing](https://github.com/jaimehisao/mogavity/actions/workflows/python-app.yml/badge.svg)](https://github.com/jaimehisao/mogavity/actions/workflows/python-app.yml)
# mogavity
## Avance #1 LéxicoSintaxis 13/04/2022
Para este avance tenemos los tokens establecidos y los igualamos a sus valores correspondientes. Además, terminamos de implementar toda las reglas gramáticales. Aparte, creamos un archivo .txt que contiene un ejemplo simple de como se puede ver nuestro programa. Lo checamos con nuestro parser y lexer, y nos marca que está correcto. Por lo tanto, en este avance tenemos el lexer y el parser listo, aunque estamos conscientes de que podamos hacer cambios a estos en un futuro.

## Avance #2 Semántica Básica de Variables y Cubo Semántico 28/04/2022
Para este avance definimos nuestro function directory. Implementamos una clase llamada function_directory la cual tiene métodos que nos van a ayudar para los puntos neuralgicos. Dentro de function_directory, también implementamos la tabla para las variables. Además, empezamos a establecer los puntos neuralgicos para operaciones básicas para las variables y funciones. Al igual, creamos y terminamos el cubo semántico. 

## Avance #3 Generación de Código para expresiones aritméticas y estatutos secuenciales 01/05/2022
Para este avance establecimos los cuadruplos y las pilas. Pudimos empezar a implementar la generación de código para las expresiones aritméticas, expresiones de operadores relacionales y lógicos. Para los estatuos secuenciales hasta el momento tenemos el de lectura y asignación. 

## Avance #4 Generación de Código para condiciones y ciclos 09/05/2022
Corregimos errores que nos generaban tanto la tabla de funciones como el cubo semántico. Terminamos de completar la generación de código para las expresiones aritméticas, operadores lógicos y operadores relacionales. Al igual, terminamos de implementar la generación de código para las condiciones y el while. Implementamos el código para el ciclo de for, pero todavía no lo probamos. Aparte, empezamos a dividir la memoria y crear funciones para asignar las variables a memoria. 

## Avance #5 Generación de Código para funciones 16/05/2022
Para este avance terminamos la generación de código del FOR. Empezamos a implementar la generación de código para las funciones, todavía no lo completamos. Se creó la clase para el manejo de memoria. Ajustamos generacion de cuadruplos para asignar espacios de memoria. El directorio de funciones ya acepta constantes y los separa en su propia tabla. 

## Avance #6 Ejecución de Expresiones y Estatutos Secuenciales. Mapa de Memoria en Ejecución 24/05/2022
Para este avance terminamos la generación de código para las funciones. Dentro de la máquina virtual ya implementamos la ejecución de expresiones y estatutos secuenciales. También ya empezamos a implementar la ejecución para las funciones, sin embargo todavía no lo terminamos. El mapa de memoria en ejecución está casi completado, solo nos falta afinar unos detalles en cuanto a los parametros para ls funciones.

## Avance #7 Generación de Código de Arreglos y Ejecución de Condicionales 30/05/2022
Para este avance implementamos la generación de código para arreglos. Se realizó la implementación de recursividad. La máquina virtual ya maneja diferentes alcances, es decir que ya puede despertar y dormir memoria para las diferentes funciones. Añadiendo a eso, ya guardamos los valores de retorno para cada llamda de función. También ya terminamos de implementar la generación de código de las funciones. 

## Avance #8 Avance de Documentación y Ejecución de Aplicación propia 03/06/2022
Para este avance terminamos de implementar todas las funcionalidades que teníamos previstos para el compilador. Tenemos pendiente arreglar algunos aspectos "estéticos" para reducir las restricciones. Iniciamos la documentación, sin embargo solo hemos podido actualizar unos cuantos diagramas y agregar sus puntos neurálgicos. 