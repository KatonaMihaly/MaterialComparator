import json
import unittest
from app import app, Material, MaterialComparator


class TestMaterialCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and example materials."""
        self.app = app.test_client()
        self.app.testing = True

        # Load materials from the JSON file
        with open("materials.json", "r") as f:
            material_data = json.load(f)

        # Select the first two materials
        self.material1 = Material.from_dict(material_data[0])
        self.material2 = Material.from_dict(material_data[1])

    def test_material_from_dict(self):
        """Test that Material objects can be created from a dictionary manually."""
        data = {"name": "M-15 Steel", "electrical_conductivity": 1.9}
        material = Material.from_dict(data)
        self.assertEqual(material.name, "M-15 Steel")
        self.assertEqual(material.electrical_conductivity, 1.9)

    def test_material_comparator(self):
        """Test the comparison of two Material objects."""
        comparator = MaterialComparator(self.material1, self.material2)
        result = comparator.compare()
        self.assertEqual(
            result,
            {"Electrical_conductivity [MS/m]": (10.44, 5.8)}
        )

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pure Iron", response.data)
        self.assertIn(b"1006 Steel", response.data)
        self.assertIn(b"M-15 Steel", response.data)

    def test_compare_route(self):
        """Test the compare route using materials.json data."""
        # Post data to the compare route
        response = self.app.post(
            "/compare",
            data=dict(material1="Pure Iron", material2="1006 Steel"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pure Iron", response.data)
        self.assertIn(b"1006 Steel", response.data)
        self.assertIn(b"10.44", response.data)
        self.assertIn(b"5.8", response.data)

    def run(self, result=None):
        """Override the run method to show test names and results."""
        test_name = self._testMethodName
        try:
            super().run(result)
            if result.wasSuccessful():
                print(f"{test_name}: Passed")
            else:
                print(f"{test_name}: Failed")
        except Exception as e:
            print(f"{test_name}: Failed with Exception: {e}")

if __name__ == "__main__":
    unittest.main()
