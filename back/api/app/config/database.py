import os

import psycopg

from psycopg import Connection

from psycopg.rows import DictRow, dict_row

from typing import Any, LiteralString

from dotenv import load_dotenv


load_dotenv();

class DataBaseException(Exception):

    _message : str;

    def __init__(self, message : str) -> None:
        self._message = message;
        super().__init__(self._message)


    @property
    def message(self) -> str:
        return self._message;

class Database():

    """Gestiona una conexión retutilizable a Postgres usando psycopg v3"""

    #Indicamos que los cursores de la conexion deben devolver diccionarios
    _connection : Connection[DictRow] | None;

    def __init__(self) -> None:
       self._connection = None;


    @property
    def isConnected(self) -> bool:
        return self._connection is not None and not self._connection.closed;


    def connect(self) -> None:
        """Abre la conexión si no existe o esta cerrada"""

        if self.isConnected:
            return;

        try:
            self._connection = psycopg.Connection[DictRow].connect(
                host=os.getenv('POSTGRES_HOST','localhost'),
                dbname=os.getenv('POSTGRES_DB'),
                user = os.getenv('POSTGRES_USER'),
                password = os.getenv('POSTGRES_PASSWORD'),
                port = os.getenv('POSTGRES_PORT','5432'),
                sslmode = os.getenv('POSTGRES_SSLMODE','require'),
                row_factory=dict_row,   
            )

        except Exception:
            raise

        
    def close(self) -> None:

        """Cerrar la conexión de forma segura"""

        if self.isConnected and self._connection is not None:
            self._connection.close();

        self._connection  = None;

    def execute(self , sql : LiteralString , params : tuple[Any, ...] | None = None ) -> list[dict[str,Any]] | None :
        """Ejecuta sentencias sql"""
        if not self.isConnected or self._connection is None:
            raise RuntimeError('No existe una conexion activa en la base de datos');

        try:

            with self._connection.cursor() as cur:
                cur.execute(sql,params);
                if cur.description is not None:
                    rows = cur.fetchall();
                else:
                    rows= [];

            self._connection.commit();

            return rows;

        except Exception:
            if self.isConnected:
                self._connection.rollback();

            raise 

    def execute_one(self, sql : LiteralString, params : tuple[Any,...] | None = None) -> dict[str,Any] | None :

        if not self.isConnected:
            raise RuntimeError('No existe Conexion a la base de datos');

        try:

            assert self._connection is not None

            with self._connection.cursor() as cur:
                cur.execute(sql,params);

                if cur.description is not None:
                    row = cur.fetchone();
                else:
                    row = {};


            self._connection.commit();
            return row;

        except Exception:

            if self.isConnected:
                self._connection.rollback(); #type: ignore

            raise;


    

        


    
