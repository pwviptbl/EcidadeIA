import psycopg2

conn = psycopg2.connect("dbname='auto_niteroi_ecidade_prod_20260429' user='ecidade' host='pgs01' port='5432' password='halegria'")
cur = conn.cursor()
try:
    cur.execute("SELECT fc_semacento('Icaraí')")
    print("fc_semacento:", cur.fetchone())
except Exception as e:
    print("Error fc_semacento:", e)
    conn.rollback()

try:
    cur.execute("SELECT unaccent('Icaraí')")
    print("unaccent:", cur.fetchone())
except Exception as e:
    print("Error unaccent:", e)
    conn.rollback()
