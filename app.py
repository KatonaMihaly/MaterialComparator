from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="html")

class Material:
    """Represents a material with physical and magnetic properties."""
    def __init__(self, name, electrical_conductivity):
        self.name = name
        self.electrical_conductivity = electrical_conductivity

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["electrical_conductivity"])

class MaterialComparator:
    """Compares two Material objects by their physical and magnetic properties."""
    def __init__(self, material1, material2):
        self.material1 = material1
        self.material2 = material2

    def compare(self):
        return {
            "Electrical_conductivity [MS/m]": (self.material1.electrical_conductivity, self.material2.electrical_conductivity)
        }

with open("materials.json") as f:
    material_data = json.load(f)
    materials = [Material.from_dict(m) for m in material_data]
@app.route("/")
def index():
    return render_template("index.html", materials=materials)

@app.route("/compare", methods=["POST"])
def compare():
    material1 = next(m for m in materials if m.name == request.form["material1"])
    material2 = next(m for m in materials if m.name == request.form["material2"])
    comparison = MaterialComparator(material1, material2).compare()
    return render_template("comparison.html", result=comparison, material1=material1.name, material2=material2.name)

if __name__ == "__main__":
    app.run(debug=True)