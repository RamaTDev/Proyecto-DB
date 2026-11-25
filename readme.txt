=====================================================================
GESTIÓN DE STOCK - Proyecto DB
PostgreSQL + API REST (FastAPI) + front web (HTML, CSS y JavaScript)
=====================================================================
Última actualización: 25/11/2026

Sistema para administrar productos, proveedores y categorías. Las
reglas del negocio (qué datos son obligatorios, qué no se puede
repetir, cuándo se puede dar de baja algo) están programadas en la
base de datos, con funciones y triggers de PostgreSQL. La API las
publica por HTTP y el front las usa desde el navegador.


CONTENIDO
---------
  1. Cómo funciona
  2. Estructura del repositorio
  3. Requisitos
  4. Puesta en marcha
  5. Uso del front (con capturas)
  6. API REST
  7. Base de datos
  8. Cómo está hecho el front
  9. Comportamientos a tener en cuenta
 10. Solución de problemas


=====================================================================
1. CÓMO FUNCIONA
=====================================================================
Diagrama: arquitectura.png

  +-----------+  HTTP / JSON  +-----------+      SQL      +------------+
  |  Front    | ------------> |   API     | ------------> | PostgreSQL |
  |  :5500    | <------------ |  :8000    | <------------ |  :5432     |
  +-----------+               +-----------+               +------------+
    navegador                    FastAPI                  base products

Ejemplo: guardar un producto desde el front.

  1. El front arma un JSON con los datos del formulario y lo manda
     a la API: PUT http://127.0.0.1:8000/products/12
  2. La API controla el formato (tipos de datos) y llama a la
     función de la base: select * from fn_updateProduct(12, ...)
  3. La función y el trigger de la tabla aplican las reglas. Si algo
     no se cumple, cortan con RAISE EXCEPTION y un mensaje.
  4. La API responde. Si la base rechazó la operación, devuelve
     status 400 con el mensaje del RAISE EXCEPTION en "detail".
  5. El front muestra un aviso verde (todo bien) o rojo (error). El
     texto del aviso rojo es exactamente el mensaje de la base.

Como los triggers están en las tablas, sus validaciones se aplican
siempre: desde el front, desde Swagger o con un INSERT o UPDATE
escrito a mano en pgAdmin.


=====================================================================
2. ESTRUCTURA DEL REPOSITORIO
=====================================================================
Proyecto-DB/
  readme.txt ................. este documento
  INSTRUCCIONES_API.txt ...... guía para levantar la API
  arquitectura.png ........... diagrama front - API - base
  capturas/ .................. capturas del front (sección 5)
  back/
    sql/ ..................... funciones, triggers y vista
      categories.sql
      suppliers.sql
      products.sql
      view.sql
    api/ ..................... API REST en Python
      requirements.txt ....... librerías necesarias
      .env ................... datos de conexión a la base (no se
                               sube a GitHub: cada uno crea el suyo)
      app/
        main.py .............. arma la app: CORS, conexión, rutas y
                               manejo de errores
        config/database.py ... conexión a PostgreSQL (psycopg 3)
        modules/
          products/ .......... rutas /products
          suppliers/ ......... rutas /suppliers
          categories/ ........ rutas /categories
          view/ .............. ruta /view (resumen con filtros)
  front/
    index.html ............... página Productos (inicio)
    proveedores.html ......... página Proveedores
    categorias.html .......... página Categorías
    resumen.html ............. página Resumen
    css/styles.css ........... estilos de las 4 páginas
    js/api.js ................ todas las llamadas a la API
    js/ui.js ................. avisos, formato de precios, etiquetas
    js/productos.js, js/proveedores.js, js/categorias.js,
    js/resumen.js ............ lógica de cada página

Los cuatro módulos de la API tienen la misma estructura:
  router.py .................. endpoints: URL, método y respuesta
  schemas.py (schema.py) ..... modelos de Pydantic: qué campos entran
                               y salen, y de qué tipo
  repository/irepository.py .. interfaz: qué operaciones existen
  repository/repository.py ... ejecuta las funciones SQL de la base
main.py crea un repositorio por módulo, se lo pasa a su router y
registra cada router con su prefijo (/products, /suppliers, etc.).


=====================================================================
3. REQUISITOS
=====================================================================
- PostgreSQL (probado con la versión 18) y pgAdmin o psql.
- Python 3.11 o superior (probado con 3.13 y 3.14). Con 3.10 la API
  no arranca: app/config/database.py usa LiteralString, que aparece
  en Python 3.11.
- Un navegador actual: Chrome, Edge o Firefox.
- Opcional: VS Code con la extensión Live Server.

Librerías de Python (back/api/requirements.txt; se instalan en el
paso 4.2): FastAPI 0.163, Pydantic 2.14, psycopg 3.3, Uvicorn 0.54
y python-dotenv 1.2.


=====================================================================
4. PUESTA EN MARCHA
=====================================================================
Orden: 1) PostgreSQL corriendo, 2) la API, 3) el front.

Los comandos son para Windows (PowerShell) y se ejecutan desde la
carpeta Proyecto-DB. En Linux o macOS, cambiar .venv\Scripts\ por
.venv/bin/ y "py" por "python3".


4.1 Base de datos
-----------------
Los scripts de back/sql no crean las tablas: agregan funciones,
triggers y la vista a una base que ya tiene las tablas products,
suppliers y categories (columnas en la sección 7.1). Para pasar la
base completa a otra computadora, usar en pgAdmin "Backup..." (clic
derecho en la base) y después "Restore..." en la otra.

  a) En pgAdmin: clic derecho en la base (la nuestra se llama
     "products") > Query Tool.
  b) Abrir cada script con el ícono de carpeta y ejecutarlo con F5,
     en este orden:
        back/sql/categories.sql
        back/sql/suppliers.sql
        back/sql/products.sql
        back/sql/view.sql

  También se puede usar psql desde la terminal (pide la contraseña;
  en Windows está en C:\Program Files\PostgreSQL\18\bin):
     psql -h localhost -U postgres -d products -f back/sql/categories.sql
     (y lo mismo con los otros tres)

Cada script se ejecuta una sola vez. Si se repite, fallan los
CREATE TRIGGER y el ALTER TABLE de categories.sql porque ya existen.
Para actualizar una función alcanza con seleccionar su bloque
CREATE OR REPLACE FUNCTION y ejecutar solo eso (en pgAdmin, F5
ejecuta únicamente el texto seleccionado).

Las columnas de texto no pueden tener NULL en las filas existentes
(por ejemplo categories.picture o suppliers.fax): la API las espera
como texto y el listado respondería error 500. Si no hay dato,
guardar '' (texto vacío).


4.2 API
-------
  cd back\api
  py -3.13 -m venv .venv          (u otra versión 3.11 o superior)
  .venv\Scripts\python.exe -m pip install -r requirements.txt

Crear el archivo back\api\.env con los datos de la base:

  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  POSTGRES_DB=products
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=<contraseña de PostgreSQL>

El .env está en .gitignore: nunca se sube a GitHub.

Levantar la API:

  .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Para comprobar que anda, abrir http://127.0.0.1:8000/docs (Swagger:
lista todos los endpoints y permite probarlos).

- No hace falta "activar" el entorno virtual: llamar directamente a
  .venv\Scripts\python.exe evita el bloqueo de scripts de PowerShell.
- La API se conecta a la base al arrancar. Si PostgreSQL no está
  corriendo o el .env tiene datos incorrectos, no arranca.
- Con --reload la API se reinicia sola cuando cambia el código. Sin
  --reload hay que cortarla (Ctrl+C) y volver a levantarla.


4.3 Front
---------
El front tiene que abrirse desde http://127.0.0.1:5500 (o
http://localhost:5500), que es el origen que la API acepta (CORS).
Abrir los archivos con doble clic (file://) no funciona.

  Opción A, VS Code: clic derecho en front/index.html >
            "Open with Live Server".
  Opción B, terminal:
              cd front
              py -m http.server 5500
            y abrir http://127.0.0.1:5500

La dirección de la API está en front/js/api.js (API_URL). Si la API
corre en otra máquina o en otro puerto, cambiarla ahí. Si el front
se sirve en otro puerto, agregarlo a allow_origins en
back/api/app/main.py (hoy acepta 5500, 5173 y 3000).


=====================================================================
5. USO DEL FRONT
=====================================================================
Las capturas están en la carpeta capturas/ (1280 px de ancho) y
muestran datos reales de la base de desarrollo.


5.1 Elementos comunes a todas las páginas
-----------------------------------------
- Barra superior para pasar de una sección a otra.
- Buscador: filtra la tabla mientras se escribe. Lo hace el
  navegador, sin volver a consultar la API.
- Filtro de estado: Todos, Activos o Dados de baja.
- Contador "N de M": filas visibles de filas totales.
- Botones de cada fila, según su estado:
    activa ............ Editar y Dar de baja
    dada de baja ...... Reactivar (la fila se ve en gris)
- "+ Nuevo..." abre el formulario vacío y "Editar" lo abre con los
  datos de la fila. "Guardar" envía y "Cancelar" cierra.
- Dar de baja pide confirmación. La baja es lógica: la fila no se
  borra y se puede reactivar.
- Avisos, arriba a la derecha:
    verde ... la operación se hizo. Se cierra solo a los 4 segundos.
    rojo .... la operación fue rechazada. Muestra el mensaje tal cual
              lo devuelve la base y queda hasta cerrarlo con la ×.
- Los formularios no validan por su cuenta: mandan los datos como
  están y la base decide. Por eso el mensaje de error es siempre el
  de la base (o el de la API, si el formato es inválido).


5.2 Productos (index.html)
--------------------------
[ capturas/01-productos.png ]
Listado de productos. Muestra el nombre del proveedor y de la
categoría (no sus IDs), el precio con formato $ 7.600,00, el stock,
las unidades en pedido, el nivel de reposición y el estado: "Activo"
o "Dado de baja", más "Descontinuado" si corresponde. El buscador
busca por nombre.

[ capturas/02-producto-editar.png ]
Formulario de edición. Los desplegables ofrecen solo proveedores y
categorías activos; si el producto tiene uno dado de baja, aparece
igual, marcado "(dado de baja)". La casilla "Descontinuado" aparece
solo al editar.

[ capturas/03-error-de-la-base.png ]
Error devuelto por la base: se intentó guardar el precio -1 y el
trigger respondió "unitprice es obligatorio y debe ser mayor o igual
a 0". El producto no se modificó.

Reglas principales (detalle y mensajes en la sección 7.2):
- Nombre obligatorio y único. Precio, stock, unidades en pedido y
  nivel de reposición obligatorios y mayores o iguales a 0.
- Al crear un producto o cambiarle el proveedor, el proveedor tiene
  que estar activo.
- Solo se puede dar de baja un producto sin stock y sin unidades en
  pedido.
- Un producto dado de baja no se puede editar hasta reactivarlo, y
  para reactivarlo su proveedor tiene que estar activo.
- "Descontinuado" no es lo mismo que "dado de baja": el producto
  sigue activo, pero no se le puede aumentar el stock ni las
  unidades en pedido.


5.3 Proveedores (proveedores.html)
----------------------------------
[ capturas/04-proveedores.png ]
Listado de proveedores: empresa, contacto (nombre y cargo), ciudad,
país, teléfono y estado. El buscador busca por empresa, contacto,
ciudad o país.

[ capturas/05-proveedor-nuevo.png ]
Formulario de alta con los 11 datos del proveedor.

Reglas principales (detalle y mensajes en la sección 7.3):
- Los 11 campos son obligatorios y el nombre de la empresa no se
  puede repetir.
- Teléfono: solo números, espacios y los signos + ( ) -.
- Un proveedor dado de baja no se puede modificar.
- Al dar de baja un proveedor, todos sus productos quedan
  descontinuados y sus unidades en pedido pasan a 0. El front lo
  advierte antes de confirmar.
- Reactivar un proveedor no les quita "descontinuado" a sus
  productos: hay que destildarlo editando cada producto.


5.4 Categorías (categorias.html)
--------------------------------
[ capturas/06-categorias.png ]
Listado de categorías: imagen, nombre, descripción y estado. Si el
campo imagen tiene una dirección web (http o https), se muestra la
miniatura; si no, el texto. El buscador busca por nombre o
descripción.

- El formulario tiene nombre, imagen (URL o nombre de archivo) y
  descripción.
- El nombre es obligatorio y no se puede repetir.
- Una categoría dada de baja no se puede modificar.
- Los avisos verdes son los textos que devuelve la base, por
  ejemplo "Categoría dada de alta correctamente.".


5.5 Resumen (resumen.html)
--------------------------
[ capturas/07-resumen.png ]
Todos los productos con su categoría, proveedor, precio, stock y
estado, ordenados por nombre. Los datos salen de la vista
vw_resumen.

[ capturas/08-resumen-filtros.png ]
Filtros combinados: no descontinuados, stock desde 25 y precio hasta
9000. Resultado: 4 productos.

Filtros (todos opcionales y combinables):
  Producto ............. parte del nombre, sin importar mayúsculas
  Categoría ............ una categoría de la lista
  Descontinuado ........ Todos, Sí o No
  Stock desde / hasta .. rango de stock (incluye los extremos)
  Precio desde / hasta . rango de precio (incluye los extremos)

"Filtrar" hace la consulta y "Limpiar" borra los filtros y vuelve a
mostrar todo. A diferencia del buscador de las otras páginas, acá
filtra la base de datos (función fn_filterView). Un rango al revés
(desde mayor que hasta) da 0 resultados, y un número negativo
muestra un error con el nombre del campo.


=====================================================================
6. API REST
=====================================================================
Dirección base: http://127.0.0.1:8000
Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

Todo se envía y se recibe en JSON. Los precios vuelven como texto
con dos decimales, por ejemplo "7600.00".


6.1 Productos - /products
-------------------------
  GET     /products/                lista todos
  GET     /products/{id}            busca uno (ver sección 9, punto 1)
  POST    /products/                crea un producto
  PUT     /products/{id}            lo modifica
  DELETE  /products/{id}            lo da de baja (active = false)
  POST    /products/{id}/activate   lo reactiva (active = true)

Respuestas: el listado devuelve {"products": [...]} y las demás
{"message": "...", "product": {...}} (201 al crear, 200 el resto).

Cuerpo de POST /products/:
  {"productname": "Queso de cabra estacionado", "supplierid": 4,
   "categoryid": 4, "quantityperunit": "horma 500 g",
   "unitprice": 7600, "unitsinstock": 20, "unitsonorder": 5,
   "reorderlevel": 8}

PUT lleva los mismos campos más "discontinued" (true o false,
obligatorio).

Producto devuelto:
  {"productid": 12, "productname": "Queso de cabra estacionado",
   "supplierid": 4, "categoryid": 4, "quantityperunit": "horma 500 g",
   "unitprice": "7600.00", "unitsinstock": 20, "unitsonorder": 5,
   "reorderlevel": 8, "discontinued": false, "active": true}


6.2 Proveedores - /suppliers
----------------------------
  GET     /suppliers/               lista todos
  GET     /suppliers/{id}           busca uno (404 si no existe)
  POST    /suppliers/               crea un proveedor
  PUT     /suppliers/{id}           lo modifica (solo si está activo)
  DELETE  /suppliers/{id}           lo da de baja y descontinúa sus
                                    productos
  POST    /suppliers/{id}/activate  lo reactiva

Respuestas: el listado devuelve {"suppliers": [...]} y las demás
{"supplier": {...}} con status 200 (también al crear).

Cuerpo de POST y PUT (11 campos de texto):
  {"companyname": "Quesería Los Molinos",
   "contactname": "Ernesto Tolaba", "contacttitle": "Productor",
   "address": "Camino a Seclantás s/n", "city": "Molinos",
   "region": "Salta", "postalcode": "4419", "country": "Argentina",
   "phone": "(3868) 494-030", "fax": "(3868) 494-031",
   "homepage": "https://www.queserialosmolinos.com.ar"}

El proveedor devuelto tiene además "supplierid" y "active".


6.3 Categorías - /categories
----------------------------
  GET     /categories/              lista todas
  GET     /categories/{id}          busca una
  POST    /categories/              crea una categoría
  PUT     /categories/{id}          la modifica
  DELETE  /categories/{id}          la da de baja (discontinued = true)
  POST    /categories/{id}          la reactiva (sin "/activate")

Respuestas: el listado devuelve {"categories": [...]}, la búsqueda
{"category": {...}} y las demás, solo el texto que devuelve la base
(201 al crear, 200 el resto):
  {"message": "Categoría dada de alta correctamente."}

Cuerpo de POST y PUT (los tres campos tienen que estar; description
y picture pueden ir vacíos):
  {"categoryname": "Lácteos",
   "description": "Quesos y lácteos artesanales",
   "picture": ""}


6.4 Resumen con filtros - /view
-------------------------------
  GET /view/   con estos parámetros opcionales en la URL:

    productname ... el nombre contiene el texto
    categoryname .. la categoría contiene el texto
    discontinued .. true o false
    stockmin ...... stock <= valor   (tope)
    stockmax ...... stock >= valor   (piso)
    pricemin ...... precio <= valor  (tope)
    pricemax ...... precio >= valor  (piso)

Ojo: "min" y "max" funcionan al revés de lo habitual; así está
definido en fn_filterView. Los números tienen que ser >= 0.

Ejemplo, productos con stock entre 5 y 100:
  http://127.0.0.1:8000/view/?stockmax=5&stockmin=100

Respuesta:
  {"filter": [{"productid": 15, "product": "Harina de algarroba",
               "price": "2900.00", "stock": 75, "category": "Harinas",
               "supplier": "Molino Andino del Norte",
               "discontinued": false, "active": true}, ...]}


6.5 Errores
-----------
  400  La base rechazó la operación: RAISE EXCEPTION de un trigger o
       de una función, u otro error de PostgreSQL. El mensaje va en
       "detail":
         {"detail": "unitprice es obligatorio y debe ser mayor o igual a 0"}

  422  El pedido no tiene la forma esperada: falta un campo, un dato
       es del tipo equivocado o un filtro es negativo. Lo detecta
       Pydantic antes de llegar a la base:
         {"detail": [{"loc": ["query", "stockmin"],
                      "msg": "Input should be greater than or equal to 0", ...}]}

  404  Búsqueda por ID sin resultado (productos y proveedores).

  500  Error no previsto; por ejemplo, un NULL en una columna de
       texto (ver 4.1).


=====================================================================
7. BASE DE DATOS
=====================================================================

7.1 Tablas
----------
  products (productos)
    productid ........ integer, clave primaria, la genera la base
    productname ...... varchar(40)
    supplierid ....... integer, referencia a suppliers
    categoryid ....... integer, referencia a categories (obligatorio)
    quantityperunit .. varchar(20)
    unitprice ........ numeric
    unitsinstock ..... integer
    unitsonorder ..... integer
    reorderlevel ..... integer
    discontinued ..... boolean, por defecto false
    active ........... boolean, por defecto true

  suppliers (proveedores)
    supplierid ....... integer, clave primaria, la genera la base
    companyname ...... varchar(40)
    contactname ...... varchar(30)
    contacttitle ..... varchar(30)
    address .......... varchar(60)
    city ............. varchar(15)
    region ........... varchar(15)
    postalcode ....... varchar(10)
    country .......... varchar(15)
    phone ............ varchar(24)
    fax .............. varchar(24)
    homepage ......... text
    active ........... boolean, por defecto true

  categories (categorías)
    categoryid ....... integer, clave primaria, la genera la base
    categoryname ..... varchar(15)
    description ...... varchar
    picture .......... text
    discontinued ..... boolean, por defecto false

Las claves primarias son columnas identity: al insertar no se manda
el ID. Si un texto supera el largo de su columna (por ejemplo, una
ciudad de más de 15 letras), el aviso de error muestra el mensaje de
PostgreSQL: "el valor es demasiado largo para el tipo character
varying(15)".

Estados:
  Dado de baja .... products.active = false, suppliers.active = false
                    o categories.discontinued = true. Es la baja
                    lógica: la fila no se borra, no se puede
                    modificar y se puede reactivar.
  Descontinuado ... products.discontinued = true. El producto sigue
                    activo, pero no se repone: no se le puede
                    aumentar el stock ni las unidades en pedido.

En las listas de abajo, cada regla va seguida del mensaje exacto de
su RAISE EXCEPTION, que es el que se ve en el front. <id>, <nombre>
y <campo> se reemplazan por el valor real.


7.2 Productos (back/sql/products.sql)
-------------------------------------
Trigger tg_validateproduct
  Se ejecuta antes de cada INSERT y UPDATE en products (función
  fntg_validateproduct). Quita los espacios de los extremos del
  nombre y de la cantidad por unidad, y controla, en este orden:

  - Nombre obligatorio.
      productname es obligatorio y no puede estar en blanco
  - Nombre único (sin distinguir mayúsculas).
      Ya existe un producto con el nombre <nombre>
  - El proveedor tiene que existir.
      El proveedor <id> no existe
  - Al crear, al cambiar de proveedor, al reactivar o al quitar
    "descontinuado", el proveedor tiene que estar activo.
      El proveedor <id> está dado de baja
  - La categoría tiene que existir.
      La categoría <id> no existe
  - Cantidad por unidad obligatoria.
      quantityperunit es obligatorio y  no puede estar en blanco
  - Precio obligatorio y >= 0.
      unitprice es obligatorio y debe ser mayor o igual a 0
  - Stock obligatorio y >= 0.
      units es obligatorio y debe ser mayor o igual a 0
  - Nivel de reposición obligatorio y >= 0.
      reorderlevel es obligatorio y debe ser mayor o igual a 0
  - Unidades en pedido obligatorias y >= 0.
      unitsinorder es obligatorio y debe ser mayor o igual a 0
  Solo al modificar:
  - Si está descontinuado, el stock no puede aumentar.
      El producto esta descontinuado, no se puede agregar más stock.
  - Si está descontinuado, las unidades en pedido no pueden
    aumentar.
      El producto esta descontinuado, no se puede agregar más unidades en orden.
  - Si está dado de baja, no pueden cambiar el stock ni las unidades
    en pedido.
      El producto esta dado de baja, no admite movimientos

Funciones que usa la API (todas devuelven la fila resultante):
  fn_insertProduct(nombre, proveedor, categoría, cantidad por
                   unidad, precio, stock, en pedido, reposición)
      Inserta el producto. Las validaciones las hace el trigger.
  fn_updateProduct(id, los mismos 8 datos, discontinued)
      No existe el producto
      El producto esta dado de baja, debes darlo de alta
  fn_deleteproduct(id): pone active = false
      Producto no encontrado
          (no existe o ya estaba dado de baja)
      El producto <nombre> todavia tiene unidades en stock
          (tiene stock o unidades en pedido)
  fn_activateproduct(id): pone active = true
      El Producto no existe
      El proveedor esta dado de baja, debes activarlo


7.3 Proveedores (back/sql/suppliers.sql)
----------------------------------------
Trigger tg_validatesupplier
  Se ejecuta antes de cada INSERT y UPDATE en suppliers (función
  fntg_validatesupplier). Quita los espacios de los extremos y
  convierte los textos vacíos en NULL. Controla:

  - Los 11 campos son obligatorios.
      <campo> es obligatorio          (ejemplo: phone es obligatorio)
  - Nombre de empresa único (sin distinguir mayúsculas).
      Ya existe un proveedor con el nombre <nombre>
  - Teléfono con números, espacios y + ( ) - solamente.
      phone tiene un formato invalido

Funciones que usa la API (todas devuelven la fila resultante):
  fn_insertsupplier(los 11 datos)
      Inserta el proveedor. Las validaciones las hace el trigger.
  fn_updatesupplier(id, los 11 datos): solo modifica proveedores
  activos
      No existe el proveedor <id>
          (no existe o está dado de baja)
  fn_deletesupplier(id): pone active = false, descontinúa todos sus
  productos y pone en 0 sus unidades en pedido
      Proveedor con id <id> no encontrado
          (no existe o ya estaba dado de baja)
  fn_activatesupplier(id): pone active = true
      El proveedor no existe


7.4 Categorías (back/sql/categories.sql)
----------------------------------------
ALTER TABLE: agrega la columna discontinued (la baja lógica).

Trigger trg_bloquear_delete_categorias
  Se ejecuta antes de cada DELETE en categories: impide borrar
  filas.
      Eliminación física no permitida en categories (ID <id>).
      Utilice la baja lógica (discontinued = true) desde el ABM.

Trigger trg_am_categorias
  Se ejecuta antes de cada INSERT y UPDATE en categories. Quita los
  espacios de los extremos del nombre y controla:
  - Nombre obligatorio.
      El nombre de la categoría no puede estar vacío.
  - Nombre único (sin distinguir mayúsculas).
      Ya existe una categoría con el nombre "<nombre>".

Función fn_abmr_categorias(acción, id, nombre, descripción, imagen)
  Una sola función para las cuatro operaciones. Devuelve un texto
  que la API pasa tal cual al front:
      A  alta ........... Categoría dada de alta correctamente.
      B  baja ........... Categoría dada de baja correctamente.
      M  modificación ... Categoría modificada correctamente.
      R  reactivación ... Categoría reactivada correctamente.
  Errores:
      Debe indicar una acción (A, B, M o R).
      Acción inválida: <acción>. Use A, B, M o R.
      Debe indicar un ID de categoría para la acción <acción>.
      El ID de categoría "<id>" no es un número válido.
      No existe la categoría con ID <id>.
      La categoría con ID <id> ya se encuentra dada de baja.      (B)
      No se puede modificar la categoría con ID <id> porque está
      dada de baja.                                               (M)
      La categoría con ID <id> ya se encuentra activa.            (R)


7.5 Resumen (back/sql/view.sql)
-------------------------------
Vista vw_resumen
  Une products, categories y suppliers. Devuelve, ordenado por
  nombre: productid, product (nombre), price (precio), stock,
  category (nombre de la categoría), supplier (empresa),
  discontinued y active.

Función fn_filterView(p_product, p_category, p_discontinued,
                      p_stockmin, p_stockmax, p_pricemin, p_pricemax)
  Devuelve las filas de vw_resumen que cumplen los filtros
  recibidos; los que llegan en NULL se ignoran. Arma la consulta con
  format(... %L ...), que pone cada valor entre comillas y evita la
  inyección SQL.


=====================================================================
8. CÓMO ESTÁ HECHO EL FRONT
=====================================================================
- HTML, CSS y JavaScript, sin frameworks ni librerías. Cada página
  carga su script como módulo: <script type="module">.
- js/api.js es el único archivo que habla con la API:
    API_URL ........ dirección de la API (http://127.0.0.1:8000)
    apiRequest() ... hace el fetch. Si la respuesta es un error, arma
                     el texto del aviso: "detail" si es un texto
                     (400) o "campo: mensaje" si es una lista (422).
    Además, una función por endpoint: getProducts(),
    createProduct(), updateSupplier(), activateCategory(),
    getResumen(), etc.
- js/ui.js: showMessage() y hideMessage() para los avisos,
  formatMoney() para los precios ($ 7.600,00), badge() para las
  etiquetas de estado y escapeHtml(), que evita que un texto
  guardado en la base se interprete como HTML.
- Cada página (productos.js, proveedores.js, categorias.js y
  resumen.js) pide sus datos, dibuja la tabla y maneja el formulario
  y los botones.
- Productos pide a la vez productos, proveedores y categorías
  (Promise.all) para mostrar nombres en lugar de IDs.
- En Productos, un campo numérico vacío se manda como null, y la
  base responde que es obligatorio.
- En Resumen, los filtros vacíos no se mandan. "Stock desde" se
  envía como stockmax y "Stock hasta" como stockmin (lo mismo con el
  precio), para respetar cómo funciona /view.


=====================================================================
9. COMPORTAMIENTOS A TENER EN CUENTA
=====================================================================
 1. GET /products/{id} usa la función fn_getproductbyid, que no está
    en back/sql: hoy responde siempre 404. El front no lo usa.
 2. Para reactivar una categoría la ruta es POST /categories/{id},
    sin "/activate" (INSTRUCCIONES_API.txt dice lo contrario).
 3. En /view, stockmin y pricemin son topes, y stockmax y pricemax
    son pisos (sección 6.4).
 4. Según los scripts del repo, reactivar un producto o un proveedor
    que ya está activo no da error: lo devuelve sin cambios. Con las
    categorías sí da error.
 5. Reactivar un proveedor no les quita "descontinuado" a sus
    productos.
 6. El trigger de productos controla que la categoría exista, pero
    no que esté activa. El front solo ofrece categorías activas.
 7. El mensaje "todavia tiene unidades en stock" aparece también
    cuando el stock es 0 pero quedan unidades en pedido.
 8. GET /categories/{id} con un ID que no existe responde 200 con
    {"error": {}}.
 9. La API abre una sola conexión a PostgreSQL al arrancar. Si se
    reinicia PostgreSQL, hay que reiniciar también la API.


=====================================================================
10. SOLUCIÓN DE PROBLEMAS
=====================================================================
Aviso "No se pudo conectar con la API. ¿Está corriendo en
http://127.0.0.1:8000?"
  La API no está levantada (paso 4.2).

El front no muestra datos y la consola del navegador (F12) habla de
CORS
  Se abrió con doble clic o desde un puerto no permitido. Abrir
  http://127.0.0.1:5500 (paso 4.3).

La API no arranca: error al conectar con PostgreSQL
  PostgreSQL no está corriendo o el .env tiene datos incorrectos.

ImportError: cannot import name 'LiteralString'
  El .venv se creó con Python 3.10 o anterior. Borrar la carpeta
  .venv y crearla de nuevo con Python 3.11 o superior.

PowerShell: "la ejecución de scripts está deshabilitada en este
sistema"
  Aparece al activar el .venv. No hace falta activarlo: usar
  .venv\Scripts\python.exe como en el paso 4.2.

GET /categories/ o /suppliers/ responde 500
  Hay un NULL en una columna de texto. Por ejemplo:
    update categories set picture = '' where picture is null;

Resumen: "no existe la función fn_filterview(...)"
  Falta ejecutar back/sql/view.sql en la base.

Un cambio en el código de la API no se ve
  La API se levantó sin --reload: cortarla con Ctrl+C y volver a
  levantarla.
