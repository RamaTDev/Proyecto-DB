
import psycopg

import os 

from dotenv import load_dotenv

load_dotenv();



with psycopg.Connection.connect(

    host = os.getenv('POSTGRES_HOST'),
    port = os.getenv('POSTGRES_PORT'),
    dbname = os.getenv('POSTGRES_DB'),
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    sslmode = 'prefer',

) as conn:

    with conn.cursor() as cur:
        cur.execute('select * from products');
        print('desde neon: ',cur.fetchall()[0]);


