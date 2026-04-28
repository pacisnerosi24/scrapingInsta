# Terea: Realizar scraping sobre una cuenta publica de instagram

### Universidad Central del Ecuador
#### Pablo Cisneros - Dispositivos Moviles P1

## Logica empleada 

En el primer intento para extraer los datos primero ocupe la libreria `requests` pero no pude obtener la infomracion deseada porque la pagina requiere loguarse para poder ver los datos, y en el segundo intento ocupe la libreria `instaloader` pero igual no pude obtener la informacion deseada  porque instagram bloquea el acceso a usuarios no autenticados aunque habia extraido mi cookie buscandola desde el dev tools del navegador (F12).

Despues de intentar con estas dos librerias busque la otra opcion de `playwright` que me da la capacidad de controlar el navegador como si fuera un usuario real y asi pude obtener la informacion deseada. Las librerias que use fueron :  
    - `playwright` para automatizar la navegacion y obtencion de datos.  
    - `json` para guardar los datos en formato json.  
    - `datetime` para guardar la fecha y hora de la extraccion.  
    - `time` para pausas en la navegacion.  
    - `random` para generar pausas aleatorias.  

Como se puede ver en el repositorio, existen dos archivos el primero es `scraper_mercado.py` que es una version simple del script para un solo usuario, y el segundo es `scrapper_users.py` que es la version que me permite scrapear varias cuentas a la vez con ayuda de una lista de usuarios.

### ¿Como lo hice?

1.  Lo primero que hice fue instalar playwright en mi entorno virtual con el comando `pip install playwright`.  
2.  Despues instale los navegadores con el comando `playwright install chromium`.
3. Al principio el script abria una ventana del navegador para mostrar el proceso, pero luego lo configure para que se ejecutara en segundo plano (headless=True), pero me di cuenta de que instagram bloquea el acceso a usuarios no autenticados, asi que tuve que iniciar sesion en instagram, al iniciar sesion igual me seguia saliendo un `error 429` que me decia que instagram detecto actividad inusual, por lo tanto no me daba los datos que queria.
4. Para contrarestar esto se me ocurrio la idea de que el script navegara por la pagina como un usuario real manteniendo el navegador abierto iniciando sesion manualmente pero despues que instagram cargara las paginas de los usuarios, extragera los datos que queria y almacenara en un archivo json. 
5. Lo primero que extraje fueron:
- nombre de usuario
- cantidad de seguidores
- cantidad de seguidos
- total de publicaciones
- biografia
6. Al ver que ya funcionaba intente descargar las publicaciones y los comentarios de cada una de ellas. 
7. Abri el dev tools del navegador (F12) y en la pestaña de network puedes ver todas las peticiones que hace la pagina, vi el preview de las fotos, di click y vi en las respues de la peticion `\info` que se formaba la estructura con las variables `pk` y `code` que me servian para poder hacer la peticion de las publicaciones y los comentarios de cada una de ellas. 
8. Pase eso al archivo `test.json` para ver mejor la estructura de la peticion y lo mismo hice con el archivo `DEBUG_RAW_leaveerickalone.json` para ver la estructura de la peticion de las publicaciones y los comentarios.
8. Los agregue las varibles a mi script que me extraiga los datos de esas variables en forma de bucle para obtner los datos de todas las publicaciones y comentarios de cada usuario.
9. Una vez obtenidos los datos los alameno en un archivo `JSON` que se guardadan con el nombre de 'estudio_nombreUsuario.json'.