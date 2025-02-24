"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os

def load_data():
    return pd.read_table("files/input/solicitudes_de_credito.csv", sep = ";", index_col= 0)


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = load_data()
    
    categorical_columns = ["sexo","tipo_de_emprendimiento","idea_negocio","tipo_de_emprendimiento", "línea_credito"]

    df["monto_del_credito"] = df["monto_del_credito"].astype(str)  # Convert to string

    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace(r"[\$,]", "", regex=True)  # Remove $ and commas
        .str.replace(r"\.00$", "", regex=True)  # Remove .00 at the end
        .str.replace(r"\.0$", "", regex=True)
    )
    df["monto_del_credito"] = df["monto_del_credito"].astype(int) 

    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")

    for column in categorical_columns:
        df[column] = df[column].str.lower()
        df[column] = df[column].str.strip()
        df[column] = df[column].str.replace(r"[\_\-]", " ", regex=True)
        df[column] = df[column].str.replace(",", "")
        df[column] = df[column].str.replace(".", "")
        df[column] = df[column].str.strip()

    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors= "coerce")
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")

    df["fecha_de_beneficio"] = pd.to_datetime(
            df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
        ).combine_first(
            pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
        )
    
    df = df.drop_duplicates()
    df = df.dropna()

    if not os.path.exists("files/output"):
        os.makedirs("files/output")
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=';', index=False)

pregunta_01()