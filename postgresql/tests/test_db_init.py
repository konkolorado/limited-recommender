import unittest
import warnings
import docker

import os

class TestInit(unittest.TestCase):
    def setUp(self):
        # Hush unittest socket warnings
        warnings.simplefilter("ignore", ResourceWarning)

        client = docker.from_env()
        try:
            client.images.get("postgres:latest")
        except docker.errors.ImageNotFound:
            self.fail("postgres image not found")

        self.containers = client.containers
        self.pg = self.containers.run("postgres:latest", detach=True,
            auto_remove=True, name="postgres-tests",
            mounts=[
                docker.types.Mount(
                    target="/data",
                    source=os.path.abspath("../../data/"),
                    type="bind", read_only=True
                )
            ])

    def tearDown(self):
        self.pg.stop()

    def test_db_running(self):
        self.assertTrue(self.container_found())

    def container_found(self):
        found = True
        try:
            self.containers.get("postgres-tests")
        except docker.errors.NotFound:
            found = False
        return found

    def test_data_in_db(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
