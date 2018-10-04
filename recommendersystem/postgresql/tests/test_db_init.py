import unittest
import warnings
import docker
import psycopg2

import os
import time

DATASRC=os.path.abspath("../../../data")
PGDATA="/var/lib/postgresql/data"
PGLOCAL="/tmp/pgdata"

booksfile = DATASRC + "/BX-Books-Cleansed-Tini.csv"
usersfile = DATASRC + "/BX-Users-Cleansed-Tini.csv"
ratingsfile = DATASRC + "/BX-Book-Ratings-Cleansed-Tini.csv"

if not os.path.exists(PGLOCAL):
    os.makedirs(PGLOCAL)

class TestInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestInit, cls).setUpClass()

        # Hush unittest socket warnings
        warnings.simplefilter("ignore", ResourceWarning)
        client = docker.from_env()

        try:
            client.images.get("postgres:latest")
        except docker.errors.ImageNotFound:
            cls.fail("postgres:latest image not found")

        cls.containers = client.containers
        cls.pg = cls.containers.run("postgres:latest", detach=True,
            auto_remove=True, name="postgres-tests", ports={"5432": "5432"},
            mounts=[
                docker.types.Mount(
                    target="/data",
                    source=DATASRC,
                    type="bind", read_only=True
                ),
                docker.types.Mount(
                    target=PGDATA,
                    source=PGLOCAL,
                    type="bind"
                )
            ])
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        cls.pg.stop()

    def test_db_running(self):
        self.assertTrue(self.container_found())

    def container_found(self):
        try:
            self.containers.get("postgres-tests")
            found = True
        except docker.errors.NotFound:
            found = False
        return found

    def test_data_in_db(self):
        self.connect_to_db()
        self.assert_data_equal("books", booksfile)
        self.assert_data_equal("users", usersfile)
        self.assert_data_equal("ratings", ratingsfile)

    def assert_data_equal(self, tablename, filename):
        n_rows = self.count_data_in_table(tablename)[0][0]
        n_lines = self.count_data_in_file(filename)
        self.assertTrue(int(n_rows) == n_lines)

    def count_data_in_table(self, table):
        return self.exec_query(f"""SELECT COUNT(*) FROM {table}""")

    def count_data_in_file(self, fname):
        with open(fname, 'r') as f:
            n_lines = sum(1 for line in f)
        return n_lines - 1 # Remove header line

    def connect_to_db(self):
        try:
            conn = psycopg2.connect(f"dbname='bookcrossing' user='bookcrossing'\
                host='localhost' password='password'")
        except:
            self.fail(f"unable to connect to bookcrossing db")
        self.cursor = conn.cursor()

    def exec_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

if __name__ == '__main__':
    unittest.main()
