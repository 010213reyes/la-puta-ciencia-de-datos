
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------

# Buscar el archivo .env en la misma carpeta que este script
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError(
        f"No se encontró MONGODB_URI en {ENV_FILE}"
    )


# ---------------------------------------------------------
# CONEXIÓN CON MONGODB ATLAS
# ---------------------------------------------------------

client = MongoClient(MONGODB_URI)

# Base de datos y colección
db = client["practica_mongodb"]
productos = db["productos"]


# ---------------------------------------------------------
# CREATE - Insertar documentos
# ---------------------------------------------------------

print("\n========== CREATE ==========")

documentos = [
    {
        "producto": "Laptop",
        "categoria": "Computo",
        "precio": 15000,
        "cantidad": 5
    },
    {
        "producto": "Mouse",
        "categoria": "Accesorios",
        "precio": 450,
        "cantidad": 20
    },
    {
        "producto": "Teclado",
        "categoria": "Accesorios",
        "precio": 850,
        "cantidad": 15
    },
    {
        "producto": "Cuaderno",
        "categoria": "Papeleria",
        "precio": 80,
        "cantidad": 30
    },
    {
        "producto": "Monitor",
        "categoria": "Computo",
        "precio": 5000,
        "cantidad": 8
    }
]

resultado = productos.insert_many(documentos)

print(
    f"Documentos insertados: "
    f"{len(resultado.inserted_ids)}"
)


# ---------------------------------------------------------
# READ - Consultar documentos
# ---------------------------------------------------------

print("\n========== READ ==========")

for producto in productos.find():
    print(
        f"{producto['producto']} | "
        f"{producto['categoria']} | "
        f"${producto['precio']} | "
        f"Cantidad: {producto['cantidad']}"
    )


# ---------------------------------------------------------
# UPDATE - Modificar un documento
# ---------------------------------------------------------

print("\n========== UPDATE ==========")

resultado = productos.update_one(
    {"producto": "Mouse"},
    {"$set": {"precio": 500}}
)

print(
    f"Documentos modificados: "
    f"{resultado.modified_count}"
)

mouse = productos.find_one(
    {"producto": "Mouse"}
)

print(
    f"Mouse actualizado -> "
    f"Precio: ${mouse['precio']}"
)


# ---------------------------------------------------------
# DELETE - Eliminar un documento
# ---------------------------------------------------------

print("\n========== DELETE ==========")

resultado = productos.delete_one(
    {"producto": "Cuaderno"}
)

print(
    f"Documentos eliminados: "
    f"{resultado.deleted_count}"
)


# ---------------------------------------------------------
# AGGREGATION - Agrupar por categoría
# ---------------------------------------------------------

print("\n========== AGGREGATION ==========")

pipeline = [
    {
        "$group": {
            "_id": "$categoria",
            "cantidad_productos": {
                "$sum": 1
            },
            "inventario_total": {
                "$sum": "$cantidad"
            },
            "valor_inventario": {
                "$sum": {
                    "$multiply": [
                        "$precio",
                        "$cantidad"
                    ]
                }
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]

resultados = productos.aggregate(pipeline)

for categoria in resultados:
    print(
        f"Categoría: {categoria['_id']} | "
        f"Productos: "
        f"{categoria['cantidad_productos']} | "
        f"Inventario: "
        f"{categoria['inventario_total']} | "
        f"Valor: "
        f"${categoria['valor_inventario']}"
    )


# ---------------------------------------------------------
# CERRAR CONEXIÓN
# ---------------------------------------------------------

client.close()

print("\n========== FIN DE LA PRACTICA ==========")
print("Conexión cerrada correctamente.")

