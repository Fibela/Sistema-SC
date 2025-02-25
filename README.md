# Sistema-SC
Sistema de Seguridad Cibernetica

Este programa/aplicacion seguridad esta destinado a prevenir un ataque o virus informatico, y tambien detener/neutralizar los ya mencionados,
Este sistema se basa de acuerdo al sistema operativo del equipo(por ejemplo: Windows(Windows defender)), calculando el uso de cpu, estado de la defensa interna junto a sus variables, actualizaciones de la misma, y archivos con terminaciones sospechosas (.dllx, .exe, entre otras).

El codigo fuente esta hecho en python, con las siguientes librerias:
~Tensorflow
~Scikit-Learn
~Pandas
~CSV
~psutil
~numpy
~json
~subprocess
~Django

Tensorflow se puso en uso para el aprendizaje claasificando datos otorgados del usuario, creando un modelo de inteligencia artifial capaz de localizar o detectar cualquier peligro dentro de el equipo,
Scikit-Learn para la estructuracion del modelo de aprendizaje de la inteligencia artificial modulando las capas neuronales del modelo y distiguir los diversos virus o ataques que pueden operarse contando caracteres y numero de columnas/filas
Pandas esta en uso para la clasificacion del flujo de datos los cuales deben ser ordenados de acuerdo a su nivel de peligro, esto en un archivo csv
CSV Formato de clasificacion de datos
psutil es la forma para monitorear el trabajo del modelo creado, puesto con este obtenemos medidas del equipo(ejemplo: Estado de red, disco de amlacenamiento)
numpy esta para el conteo de variaciones en el numero de caracteres estblacedios en nuestra base de datos clasificada, basicamente para las operaciones matematicas dentro del modelo de aprendizaje
json este tiene como funcion la transmision de pagina en base a la recepcion de datos en el codigo fuente, para la compresion intuitiva del cualquier cliente
subprocess este modulo se coloco aqui para la ejecucion de comandos dentro de el codigo, este no es esecenical para el manejo de herramientas dentro del sistema que no esten disponibles en el codigo de python
Django este framework utilizado para este proyecto, puesto que este soporta no solo el desarollo sino que tambien la produccion del programa, y en base a este se podra lanzar la version comercial del servicio a todas las y los individuos o compañias que desean un servicion de proteccion dentro de sus dispositivos elecetronicos

El sistema SC tiene una base de datos en la cual se basara para el analisis de los quipos, pero si por algun motivo no se encuentra el virus o ataque dentro de la base de datos, este lo recopilara(sin que haya duplicados de entradas de datos)para su futura prevencion y detencion

El servidor para el funcionamiento del sistema SC es uno denominado daphne para que no tengo errores el codigo y funcione a su maxima capacida el websocket dentro del servidor asgi
