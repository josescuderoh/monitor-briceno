# Plataforma de Integración de la Cooperación en el municipio de Briceño, Antioquia.

Este es el código fuente de la plataforma de integración de la cooperación el municipio de Briceño.

## Ejecución del worker redis para envío de confirmación de correos.

Para correr el servidor redis-server (cuando ya ha sido instalado) se ejecuta el siguiente comando
en la consola desde la raíz del proyecto de django

celery worker -A monitor_briceno --loglevel=debug --concurrency=4


## Instalación de las dependencias del paquete de celery

To install redis on server
sudo apt-get install redis-server

To run redis server:
redis-server

To install dependencies for gdal
sudo apt-get install libgdal-dev
