import unittest
import win32com.client

class TestExcelCOM(unittest.TestCase):
    def test_excel_dispatch(self):
        try:
            # Attempt to open an instance of Excel
            excel = win32com.client.Dispatch("Excel.Application")
            self.assertIsNotNone(excel, "Failed to create Excel object")
            
            # Optional: Make it visible and then close it
            excel.Visible = True
            excel.Quit()
        except Exception as e:
            self.fail(f"COM Verification Failed: {e}")

if __name__ == '__main__':
    unittest.main()