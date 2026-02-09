import unittest
import win32com.client
from win32com.client import constants

class TestAutoCADCOM(unittest.TestCase):
    def test_autocad_connection(self):
        """Test connection to a running AutoCAD instance and verify early binding constants."""
        try:
            # Attempt to get the active AutoCAD application object
            # Note: This requires AutoCAD to be running.
            acad = win32com.client.GetActiveObject("AutoCAD.Application")
            self.assertIsNotNone(acad, "Failed to get AutoCAD Application object")
            
            # Verify connectivity by accessing basic properties
            self.assertTrue(hasattr(acad, 'Name'), "AutoCAD object should have a 'Name' property")
            self.assertTrue(hasattr(acad, 'ActiveDocument'), "AutoCAD object should have an 'ActiveDocument' property")
            
            # Check if constants (Early Binding) are loaded correctly
            # 'acRed' is a standard AutoCAD color constant
            self.assertTrue(hasattr(constants, 'acRed'), "AutoCAD constants (Early Binding) not loaded. 'acRed' missing.")
            
        except Exception as e:
            # If AutoCAD is not running, GetActiveObject will raise an exception.
            # In a real CI environment, this might be skipped or mocked, 
            # but for this conversion, we'll report the failure or instructions.
            self.fail(f"AutoCAD COM Verification Failed: {e}. Ensure AutoCAD is running.")

if __name__ == '__main__':
    unittest.main()
