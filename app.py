"""
This module provides a Flask-based web application to compare the properties
of various materials. The application reads materials from a JSON file,
displays them on the index page, and allows the user to compare their properties.
"""

import json
from dataclasses import dataclass
from flask import Flask, render_template, request

# Flask app initialization
app = Flask(__name__, template_folder="html")

@dataclass
class Material:
    """
    Represents a material with specific properties such as electrical conductivity.

    Attributes:
        name (str): The name of the material.
        electrical_conductivity (float): The electrical conductivity of the material (in MS/m).
    """

    def __init__(self, name, electrical_conductivity):
        """
        Initializes a Material instance.

        Args:
            name (str): The name of the material.
            electrical_conductivity (float): The electrical conductivity of the material.
        """
        self.name = name
        self.electrical_conductivity = electrical_conductivity

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Material instance from a dictionary.

        Args:
            data (dict): A dictionary containing "name" and "electrical_conductivity" keys.

        Returns:
            Material: A Material instance created from the dictionary.
        """
        return cls(data["name"], data["electrical_conductivity"])


class MaterialComparator:
    """
    Compares two Material objects based on their properties such as electrical conductivity.

    Attributes:
        material1 (Material): The first material to be compared.
        material2 (Material): The second material to be compared.
    """

    def __init__(self, material1, material2):
        """
        Initializes a MaterialComparator instance.

        Args:
            material1 (Material): The first material to compare.
            material2 (Material): The second material to compare.
        """
        self.material1 = material1
        self.material2 = material2

    def compare(self):
        """
        Compares the properties of the two materials.

        Returns:
            dict: A dictionary where each key is a material property, and the value
                  is a tuple containing the values of that property for both materials.
        """
        return {
            "Electrical_conductivity [MS/m]": (self.material1.electrical_conductivity,
                                               self.material2.electrical_conductivity)
        }

    def compare_bh(self):
        """
        For later development.
        """


# Load materials from JSON file
with open("materials.json", encoding="utf-8") as f:
    material_data = json.load(f)
    materials = [Material.from_dict(m) for m in material_data]


@app.route("/")
def index():
    """
    Renders the index page with the list of materials.

    Returns:
        str: Rendered HTML page for the index route.
    """
    return render_template("index.html", materials=materials)


@app.route("/compare", methods=["POST"])
def compare():
    """
    Handles the comparison of two materials selected by the user via a POST request.

    Args:
        material1 (str): The name of the first material (from the form data).
        material2 (str): The name of the second material (from the form data).

    Returns:
        str: Rendered HTML page displaying the comparison results of the two materials.
    """
    material1 = next(m for m in materials if m.name == request.form["material1"])
    material2 = next(m for m in materials if m.name == request.form["material2"])
    comparison = MaterialComparator(material1, material2).compare()
    return render_template("comparison.html", result=comparison,
                           material1=material1.name, material2=material2.name)


if __name__ == "__main__":
    """
    Main entry point of the application. Runs the Flask web server
    in debug mode for development purposes.
    """
    app.run(debug=True)
