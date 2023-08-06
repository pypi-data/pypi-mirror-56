from sqlconnection import postgresql_queries, postgresql

if __name__ == '__main__':
    psql = postgresql.Postgresql()
    conn = psql.connection
    #psql.close_connection()

    query = "SELECT * from  retailer;"
    x = postgresql_queries.execute_query(conn, query)
    del conn
    del psql.connection
    y = 'u'
    z= psql.connection
    a = z
