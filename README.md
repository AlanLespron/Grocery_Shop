# Grocery_Shop
Repo proyecto final de Arquitectura de software

## Instalación

1. Clona este repositorio:

2. Crea un entorno virtual

3. Activa el entorno virtual:

4. Instala las dependencias:

    pip install -r requirements.txt
    

5. Configura la base de datos:

    - Asegúrate de tener un servidor PostgreSQL en ejecución.
    - Configura la URL de la base de datos en `app.py`:

        python
        DATABASE_URL = "postgresql://tu-usuario:tu-contraseña@localhost/tu-base-de-datos"
        

    - Ejecuta el script para cargar datos de ejemplo:

        python scripts/load_data_script.py
        

## Uso

1. Ejecuta la aplicación:

    python load_data_script.py
   
    python app.py
    

2. Abre tu navegador y accede a [http://localhost:5000](http://localhost:5000).


## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación Flask.
- `scripts/load_data_script.py`: Script para cargar datos de ejemplo en la base de datos.
- `templates/`: Carpeta que contiene las plantillas HTML.
- `static/css`: Carpeta que contiene el archivo css.
- `venv/`: Carpeta del entorno virtual.
- `requirements.txt`: Lista de dependencias del proyecto.


### Preguntas
¿Cuales son el top 5 de caracteristicas de arquitectura del diseño actual de tu proyecto? 

1. *Monolito Efectivo:*
   - Justificación: El diseño actual sigue una arquitectura monolítica eficiente para una aplicación pequeña y simple, facilitando el desarrollo y la mantenibilidad.

2. *Capa de Datos con ORM:*
   - Justificación: Se utiliza SQLAlchemy como ORM para interactuar con la base de datos PostgreSQL, proporcionando una capa de abstracción que facilita las operaciones CRUD.

3. *Rutas y Controladores en Flask:*
   - Justificación: Flask se utiliza para manejar las rutas y controladores de la aplicación de manera simple y eficaz, proporcionando una estructura clara para el manejo de solicitudes HTTP.

4. *Uso de Plantillas HTML:*
   - Justificación: La aplicación utiliza plantillas HTML para la representación de las vistas, siguiendo el patrón Modelo-Vista-Controlador (MVC) de Flask.

5. *Base de Datos Relacional:*
   - Justificación: PostgreSQL se utiliza como base de datos relacional, adecuada para la estructura de datos tabulares de la aplicación.

¿Si la aplicacion migrara a una arquitectura de microservicios, ¿Cuales serian el top 5 de caracteristicas de arquitectura?

1. *Arquitectura Basada en Servicios:*
   - Justificación: Se migraría a una arquitectura de microservicios para mejorar la escalabilidad y la independencia de los componentes, permitiendo el desarrollo, implementación y escalado independientes de servicios específicos.

2. *API Gateway:*
   - Justificación: Se implementaría un API Gateway para gestionar las solicitudes y enrutarlas a los microservicios correspondientes, proporcionando un punto de entrada centralizado.

3. *Contenedores Docker:*
   - Justificación: La aplicación y sus microservicios se empaquetarían en contenedores Docker para garantizar la consistencia en diferentes entornos y facilitar la implementación.

4. *Orquestación con Kubernetes:*
   - Justificación: Se utilizaría Kubernetes para la orquestación de contenedores, facilitando la implementación, la escalabilidad automática y la gestión de recursos.

5. *Autenticación y Autorización Descentralizadas:*
   - Justificación: Cada microservicio manejaría su propia autenticación y autorización, permitiendo un mmejor control y mejorando la seguridad en un entorno distribuido.
