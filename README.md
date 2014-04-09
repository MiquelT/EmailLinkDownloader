# Email Link Downloader
=========

Email Link Downloader es un script hecho en python que permite conectarse a una cuenta de correo y crear un fichero con todos los links que encuentre en los emails que esten identificados por los labels especificados entre dos fechas.
También puede descargar directamente los archivos de los links.

Instrucciones
------------
Editar el fichero config.xml con los datos de tu email:


  <conf>
  
    <!-- configuracion del email -->
    <email>
        <!-- tipo de conexion -->
        <config>
            <ssl>imap.gmail.com</ssl> <!-- imap.gmail.com para gmail -->
        </config>
        <!-- autentificacion -->
        <auth>
            <user>suemaillist@gmail.com</user>
            <password>PASSWORD</password>
        </auth>
    </email>


    <!-- aqui hay que poner todos los labels por los que se quiere buscar -->
    <labels>
        <label>pruebas</label>
        <label>label2</label>
    </labels>


    <!-- directorio en el que queremos poner las descargas -->
    <dir>archivos/</dir>

 </conf>


Una vez configurado ejecutamos el script:

`python emailLinkDownloader.py`

Opciones:
------------

* -d : descargará los archivos de los links que encuentre.
* -i : Fecha de inicio de búsqueda de emails.
* -e : Fecha de finalización de búsqueda de emails.

Dependencias
------------
* Python 2 (2.7 should be sufficient)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil) version 2.2
* [Argparse](https://docs.python.org/2/howto/argparse.html) version 1.2.1

License
-------
Esta obra está sujeta a la licencia [Reconocimiento-NoComercial 4.0 Internacional de Creative Commons](http://creativecommons.org/licenses/by-nc/4.0/). Para ver una copia de esta licencia, visite visite[http://creativecommons.org/licenses/by-nc/4.0/](http://creativecommons.org/licenses/by-nc/4.0/).


Como puede ayudar
----------------

Si encuentra cualquier error o problema puede [contactar conmigo en Twitter](https://twitter.com/miqueltur) o por [email](mailto:miquel.tur.m@gmail.com).