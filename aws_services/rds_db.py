import psycopg2


class RDS:
    def __init__(self, host, database, user, password):
        self.engine = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def fetch_data(self):
        cursor = self.engine.cursor()
        cursor.execute("select * from some_table where status in ('active', 'pending')")
        ads_data = cursor.fetchall()
        rows = [dict(zip([key[0] for key in cursor.description], row)) for row in ads_data]

        actions_list_data = []
        for data in rows:
            actions_list_data.append({
                "id": data.get("id"),
                "user": data.get("user"),
                "email": data.get("email"),
                "params": data.get("params"),
            })

        return actions_list_data

    def update_data(self, id):
        cursor = self.engine.cursor()
        query = """update some_table set email = 'alpha@gmail.com' where id = '%d'""" % id
        cursor.execute(query)
        self.engine.commit()
        return True
