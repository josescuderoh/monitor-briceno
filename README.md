## Plataforma de Integración de la Cooperación en el municipio de Briceño, Antioquia.

Este repositorio contiene el código fuente de la plataforma de integración de la cooperación el municipio de Briceño, la cual se puede encontrar en www.briceno-antioquia.gov.co

##Notas de desarrollo

### Ejecución del worker redis para envío de confirmación de correos.

Para correr el servidor redis-server (cuando ya ha sido instalado) se ejecuta el siguiente comando en la consola desde la raíz del proyecto de django

Para ejecutar el celery beat y celery worker se ejecuta el siguiente comando

```python
celery worker -A monitor_briceno -B --loglevel=info
```
