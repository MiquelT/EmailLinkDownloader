# Email Link Downloader
=========

Email Link Downloader es un script hecho en python que permite conectarse a una cuenta de correo y descargarse automáticamente todos los links que encuentre en los emails que contengan el los labels especificados:

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

    <!-- Aqui se guardara el timestamp del ultimo email leido. NO MODIFICAR -->
    <lastDownloads>

    </lastDownloads>

    <!-- directorio en el que queremos poner las descargas -->
    <dir>archivos/</dir>

 </conf>


Una vez configurado ejecutamos el script:

`python emailLinkDownloader.py`

Dependencias
------------
* Python 2 (2.7 should be sufficient)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil) version 2.2

License
-------
.


Como puede ayudar
----------------

Si encuentra cualquier error o problema puede [contactar conmigo en Twitter](https://twitter.com/miqueltur) o por [email](mailto:miquel.tur.m@gmail.com).