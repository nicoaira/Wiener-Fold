# Wiener-Fold

Uno de los problemas del EXPAR es su alta amplificación inespecífica. Un posible mecanismo de como ocurre esto podría ser mediante la formación de estrucutras secuenciarias en el Template X que puedan dejar un extremo 3' sobre si mismo para llevar a cabo una amplificación. Esto produce un trigger X que luego dispararía la reacción inespecíficamente. 

Una manera de abordar esto es usar un segundo template (denominmado template Y). El primer template X tiene su secuencia condicionada por la secuencia nativa que se encuentra en el target. Esto hace que durante el diseño del mismo a veces sea complicado encontrar una secuencia que minimice la formación de estrucutras secuendarias. Por esto, se propuso un mecanimo en el que el template X no conste de dos secuencias X'-X', sino de una secuencia híbrida X'-Y'. Una vez que aparece el trigger X, se copia la secuencia Y, que servirá como trigger para un segundo template que tendrá la secuencia Y'-Y'. Esta ultima será una secuencia optimizada para tener el minimo de estructuras secuenciarias posibles. De esta manera, solo se debe poner una concentración infima de la seuencia X'-Y' y la que se pondrá en altas concentraciones será la secuencia Y'-Y' optimaizada.

Winer-Fold es un pipeline que costa de los siguientes pasos:

1- Generacion de secuencias random, con restricciones en cuanto a:

* Longitud
* Contenido GC
* Disminución de la probabilidad de la parición de la misma base consecutivamente

2- Analisis de formación de hairpins de las secuencias mediante UNAFold. En esta instancia, un bot introduce batches de secuencias en una app web de UNAFold. Luego del análsis, se colectan los parámetros termodinamicos (cantidad de estructuras del tipo hairpin formadas y sus respectivos ΔG.

3- Analisis de formación de homodímeros de las secuencias mediante OligoAnalizer (IDT). Un bot introduce las secuencias la herramienta de IDT y obtiene las estructuras de homodímeros que puede formar cada secuencia. Luego del análsis, se colectan los parámetros termodinamicos (cantidad de estructuras de dímeros formadas y sus respectivos ΔG).

4- Clasificiación de las mejores secuencias (según los análisis termodinámicos) en clase I o clase II (buena o mala performance en EXPAR, respectivamente). Para esto se utilizarán 3 clasificadores distintos. 2 de ellos son reporoducciones de los clasificiadores utilziados en el paper "Sequence dependence of isothermal DNA amplification via EXPAR" (Gang Yi et. al, 2012): uno es un SVM y un clasificador Naive Bayes. El 3ero es un modelo de deep learning (Deep-EXPAR) desarrollado para este proyecto. 

Una vez obtenida las predicciones de los 3 clasificadores, se analizarán experimentalmente aquellas secuencias que hayan sido clasificadas como clase I en los tres casos.
