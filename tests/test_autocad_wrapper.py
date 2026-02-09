import unittest
import win32com.client

# 1. Import the file you generated.
# This registers the library and makes constants available via this module.
import AutoCAD_Wrapper


class TestAutoCADCOM(unittest.TestCase):
    def test_autocad_connection(self):
        try:
            # 2. Use the wrapper's constants directly instead of win32com.client.constants
            # This is more robust because it doesn't rely on the global cache state.
            expected_color = AutoCAD_Wrapper.constants.acRed

            acad = win32com.client.GetActiveObject("AutoCAD.Application")

            # Verify basic props
            self.assertTrue(hasattr(acad, 'Name'))

            # 3. Verify constants using the explicit module
            self.assertTrue(hasattr(AutoCAD_Wrapper.constants, 'acRed'),
                            "Constants should be loaded from the wrapper file.")

            print(f"Success! Red is defined as: {expected_color}")

        except Exception as e:
            self.fail(f"Failure: {e}")

if __name__ == '__main__':
    unittest.main()
