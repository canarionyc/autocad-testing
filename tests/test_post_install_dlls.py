import unittest
import pythoncom
import win32api

class TestPostInstallDLLs(unittest.TestCase):
    def test_pythoncom_import(self):
        self.assertIsNotNone(pythoncom.__file__, "pythoncom should have a __file__ attribute")
        
    def test_win32api_import(self):
        self.assertIsNotNone(win32api.__file__, "win32api should have a __file__ attribute")

if __name__ == '__main__':
    unittest.main()
