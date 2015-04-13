import unittest


import sys
sys.path.append('/Users/renee/Projects/personal-projects/Pwitter')
from service import app
from base_test import BaseTest



class BaseResourceTest(BaseTest):

    def test_verify_pw_success(self):

        verified = app.verify_pw("USf1ffeba94bf041", "3c7dbf890b764f23")
        print verified
        assert verified == True







if __name__ == '__main__':
    unittest.main()