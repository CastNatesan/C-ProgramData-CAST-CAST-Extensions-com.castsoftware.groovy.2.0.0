import unittest
from cast.application.test import run
from cast.application import create_postgres_engine
import logging

logging.root.setLevel(logging.DEBUG)

class TestIntegration(unittest.TestCase):

    def test2(self):
        
        run(kb_name='u320_salcus_new_local', application_name='U320 - SALCUS', engine=create_postgres_engine())


if __name__ == "__main__":
    unittest.main()
