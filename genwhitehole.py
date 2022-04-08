import database
import datetime
import math
import xml.etree.ElementTree as ET


def generate():
    db = database.load_database()

    root = ET.Element("database")
    timestamp = math.floor(datetime.datetime.now().timestamp())
    root.set("timestamp", str(timestamp))

    # Write categories
    categories = ET.SubElement(root, "categories")
    category_indices = dict()

    for i, (key, value) in enumerate(db.categories.items()):
        category_indices[key] = i
        category = ET.SubElement(categories, "category", {"id": str(i)})
        category.text = value

    # Write objects
    for key, value in db.objects.items():
        obj = ET.SubElement(root, "object", {"id": value["InternalName"]})
        clazz = db.classes[value["ClassName"]]

        flags = {
            "games": str(value["Games"]),
            "known": "1" if value["Progress"] > 0 else "0",
            "complete": "1" if value["Progress"] > 1 else "0",
            "paths": "1" if "Rail" in clazz["Parameters"] and clazz["Parameters"]["Rail"]["Needed"] else "0",
            "switches": "0",  # Not needed yet
            "fieldReqs": "0"  # Idk what this is even for...
        }

        ET.SubElement(obj, "name").text = value["Name"]
        ET.SubElement(obj, "flags", flags)
        ET.SubElement(obj, "category", {"id": str(category_indices[value["Category"]])})
        ET.SubElement(obj, "preferredfile", {"name": clazz["List"].replace("Info", "")})
        ET.SubElement(obj, "notes").text = clazz["Notes"] + "\n" + value["Notes"]
        ET.SubElement(obj, "files")   # Not used yet
        ET.SubElement(obj, "sounds")  # Not used yet

        for i in range(8):
            arg = f"Obj_arg{i}"

            if arg in clazz["Parameters"]:
                info = clazz["Parameters"][arg]

                if len(info["Exclusives"]) and key not in info["Exclusives"]:
                    continue

                arginfo = {
                    "id": str(i),
                    "type": "int" if info["Type"] == "Integer" else "float" if info["Type"] == "Float" else "bool",
                    "name": info["Name"],
                    "values": ", ".join([f"{l['Value']} = {l['Notes']}" for l in info["Values"]]),
                    "notes": info["Description"]
                }
                ET.SubElement(obj, "field", arginfo)

    # Write contents to XML
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("objectdb.xml", encoding="utf-8")


if __name__ == '__main__':
    generate()
