import pandas as pd
import sqlite3
from pathlib import Path


def main():
    # ===== EXTRACT =====
    # Leer los datos desde la fuente CSV
    BASE_DIR = Path(__file__).resolve().parent
    CSV_PATH = BASE_DIR / "ventas.csv"

    df = pd.read_csv(CSV_PATH)

    print("EXTRACT")
    print("Extraídas", len(df), "filas")

    # ===== TRANSFORM =====
    # Crear una nueva feature: ingreso total por venta
    df["total"] = df["precio"] * df["cantidad"]

    # Crear dimensión de categorías
    dim_categoria = pd.DataFrame({
        "categoria": df["categoria"].unique()
    })

    dim_categoria["cat_id"] = range(
        1,
        len(dim_categoria) + 1
    )

    # Crear tabla de hechos
    fact = df.merge(
        dim_categoria,
        on="categoria"
    )

    fact_ventas = fact[
        [
            "producto",
            "cat_id",
            "precio",
            "cantidad",
            "total"
        ]
    ]

    print("\nTRANSFORM")
    print("Feature creada: total")
    print("\nDimensión de categorías:")
    print(dim_categoria)

    print("\nTabla de hechos:")
    print(fact_ventas)

    # ===== LOAD =====
    # Crear/conectar la base de datos SQLite
    conn = sqlite3.connect("almacen.db")

    dim_categoria.to_sql(
        "dim_categoria",
        conn,
        if_exists="replace",
        index=False
    )

    fact_ventas.to_sql(
        "fact_ventas",
        conn,
        if_exists="replace",
        index=False
    )

    print("\nLOAD")
    print("Datos cargados en SQLite.")

    # ===== CONSULTA ANALÍTICA =====
    query = """
    SELECT
        d.categoria,
        COUNT(*) AS num_ventas,
        SUM(f.total) AS ingresos
    FROM fact_ventas f
    JOIN dim_categoria d
        ON f.cat_id = d.cat_id
    GROUP BY d.categoria
    ORDER BY ingresos DESC
    """

    resultado = pd.read_sql(query, conn)

    print("\nCONSULTA ANALÍTICA")
    print(resultado.to_string(index=False))

    conn.close()


if __name__ == "__main__":
    main()