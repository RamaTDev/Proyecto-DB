GESTIÓN DE STOCK - Proyecto DB
PostgreSQL + API REST (FastAPI) + front web (HTML, CSS y JavaScript)
Última actualización: 25/11/2026

Versión con capturas e imágenes incrustadas: README.md (GitHub la muestra
al abrir el repositorio). Este .txt es el resumen en texto plano.

Sistema para administrar productos, proveedores y categorías. Las reglas de
negocio (datos obligatorios, nombres únicos, bajas lógicas) están en la base
de datos, la API las publica por HTTP y el front las usa desde el navegador.

Arquitectura: arquitectura.png
    Front (:5500) -> API FastAPI (:8000) -> PostgreSQL (:5432)

QUE INCLUYE
- Base products: 3 tablas, 15 funciones, 3 triggers y la vista vw_resumen.
  Scripts en back/sql/ y dump en back/db/products.dump.
- API REST: /products, /suppliers, /categories y /view. Swagger en
  http://127.0.0.1:8000/docs.
- Front: 4 páginas sin frameworks: Productos, Proveedores, Categorías y
  Resumen.

ESTRUCTURA
  README.md / readme.txt   este resumen
  INSTRUCCIONES_API.txt    guía completa de la API
  arquitectura.png         diagrama
  capturas/                8 capturas del front
  back/db/products.dump    backup de la base
  back/sql/                categories, suppliers, products y view
  back/api/                FastAPI (app/main.py, app/modules/, .env)
  front/                   index, proveedores, categorías y resumen

PUESTA EN MARCHA
1) Base de datos: crear products y ejecutar en este orden:
     psql -h localhost -U <usuario> -d products -f back/sql/categories.sql
     psql -h localhost -U <usuario> -d products -f back/sql/suppliers.sql
     psql -h localhost -U <usuario> -d products -f back/sql/products.sql
     psql -h localhost -U <usuario> -d products -f back/sql/view.sql
   También se puede restaurar: pg_restore -d products back/db/products.dump

2) API (desde back/api, Python 3.11 o superior):
     py -3.13 -m venv .venv
     .venv\Scripts\python.exe -m pip install -r requirements.txt
     .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   Crear back/api/.env con POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,
   POSTGRES_USER y POSTGRES_PASSWORD (no se sube a GitHub).
   En Linux usar python3 y .venv/bin/.

3) Front: abrir front/index.html con Live Server en
   http://127.0.0.1:5500 (o python3 -m http.server 5500 dentro de front/).
   Abrir con doble clic no funciona por CORS.

CAPTURAS (se ven incrustadas en README.md)
  capturas/01-productos.png         listado de productos
  capturas/02-producto-editar.png   formulario de edición
  capturas/03-error-de-la-base.png  error de validación de la base
  capturas/04-proveedores.png       listado de proveedores
  capturas/05-proveedor-nuevo.png   alta de proveedor
  capturas/06-categorias.png        listado de categorías
  capturas/07-resumen.png           vista resumen
  capturas/08-resumen-filtros.png   resumen con filtros

API REST
  Base: http://127.0.0.1:8000  -  Swagger: /docs  -  respuestas en JSON

  GET / POST                  /products/             listar / crear
  GET / PUT / DELETE          /products/{id}         buscar / modificar / baja
  POST                        /products/{id}/activate  reactivar
  GET / POST                  /suppliers/            listar / crear
  GET / PUT / DELETE          /suppliers/{id}        buscar / modificar / baja
  POST                        /suppliers/{id}/activate reactivar
  GET / POST                  /categories/           listar / crear
  GET / PUT / DELETE          /categories/{id}       buscar / modificar / baja
  POST                        /categories/{id}       reactivar
  GET                         /view/                 resumen filtrado

  /view/ acepta productname, categoryname, discontinued, stockmin,
  stockmax, pricemin y pricemax. Ojo: min es tope (<=) y max es piso (>=),
  según fn_filterView. Ejemplo: /view/?stockmax=5&stockmin=100 devuelve
  stock entre 5 y 100.
  Detalle completo: INSTRUCCIONES_API.txt.

BASE DE DATOS
- products: alta, baja lógica (active), edición y reactivación.
  Trigger tg_validateproduct.
- suppliers: la baja lógica descontinúa sus productos.
  Trigger tg_validatesupplier.
- categories: baja lógica con discontinued y bloqueo de borrado físico.
  Trigger trg_am_categorias.
- vw_resumen y fn_filterView alimentan la página Resumen y /view.

A TENER EN CUENTA
- Dar de baja no borra la fila: se puede reactivar.
- discontinued no es lo mismo que inactivo: el producto sigue activo pero
  no se le aumenta stock.
- Los mensajes de error del front vienen de los RAISE EXCEPTION de PostgreSQL.
- La API abre una conexión al arrancar: si se reinicia PostgreSQL, reiniciar
  también la API.
