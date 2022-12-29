## Como instalar el proyecto
- Clonar el repositorio
```
C:\>git clone url_del_proyecto
```
- Entrar a la carpeta del repositorio clonado: 
```
C:\>cd proyecto
```
- Una vez clonado, crear un entorno virtual
```
C:\proyecto>python -m venv "venv"
```
- Activar el entorno virtual
```
C:\proyecto>cd venv
C:\proyecto\venv\>cd Scripts
C:\proyecto\venv\Scripts>activate
```
- Volver a la carpeta donde se clono el proyecto:
```
(venv) C:\proyecto\venv\Scripts>cd ..
(venv) C:\proyecto\venv>cd ..
(venv) C:\proyecto>
```
- Una vez activado el entorno virtual y estando en la carpeta del proyecto se instalan los requerimientos
```
(venv) C:\proyecto>pip install -r requirements.txt
```


## Ejecutar el programa
- Se inicializa la base de datos con el siguiente comando:
```
(venv) C:\proyecto>flask --app parking_payment init-db
```
Deberá mostrar lo siguiente:
```
(venv) C:\proyecto> La base de datos se ha inicializado con exito!
```
- Para poner en marcha el programa ingresamos el suigueinte comando: 
```
(venv) C:\proyecto>flask --app parking_payment run --debugger
```

#
Nota: Seguir los pasos como se muestran