import database
import datetime
import math
import xml.etree.ElementTree as ET

__FIELD_TYPES__ = {"Integer": "int", "Float": "float", "Boolean": "bool"}


def generate(db):
    # Create "database" root element
    timestamp = math.floor(datetime.datetime.now().timestamp())
    node_root = ET.Element("database")
    node_root.set("timestamp", str(timestamp))

    # Create category elements
    category_indices = dict()
    node_categories = ET.SubElement(node_root, "categories")

    for i, (category_id, category_desc) in enumerate(db.categories.items()):
        category_indices[category_id] = i
        ET.SubElement(node_categories, "category", {"id": str(i)}).text = category_desc

    # Create object elements. Whitehole does not differentiate between objects and actors, so we have to combine them...
    for obj_name, obj_info in db.objects.items():
        node_object = ET.SubElement(node_root, "object", {"id": obj_info["InternalName"]})

        # Also another limitation of Whitehole's older format. We will use SMG2's class due to being more famous.
        class_info = db.classes.get(obj_info["ClassNameSMG2"], None)

        flags = {
            "games": str(obj_info["Games"]),
            "known": str(int(obj_info["Progress"] > 0)),
            "complete": str(int(obj_info["Progress"] > 1)),
            "needsPaths": str(int(class_info is not None and "Rail" in class_info["Parameters"] and class_info["Parameters"]["Rail"]["Needed"]))
        }

        class_notes = "" if class_info is None else class_info["Notes"]
        notes = f'-- OBJECT NOTES --\n{obj_info["Notes"]}\n\n-- CLASS NOTES --\n{class_notes}'

        ET.SubElement(node_object, "name").text = obj_info["Name"]
        ET.SubElement(node_object, "flags", flags)
        ET.SubElement(node_object, "category", {"id": str(category_indices[obj_info["Category"]])})
        ET.SubElement(node_object, "preferredfile", {"name": obj_info["ListSMG2"].replace("Info", "")})
        ET.SubElement(node_object, "notes").text = notes
        ET.SubElement(node_object, "files")  # UseResource stuff is outside the DB's scope

        if class_info is None:
            continue

        for i in range(8):
            arg_name = f"Obj_arg{i}"

            if arg_name in class_info["Parameters"]:
                arg_info = class_info["Parameters"][arg_name]

                # Only append to objects that support this field
                if len(arg_info["Exclusives"]) and obj_name not in arg_info["Exclusives"]:
                    continue

                values = ", ".join([f"{l['Value']} = {l['Notes']}" for l in arg_info["Values"]])

                arg_attrs = {
                    "id": str(i),
                    "type": __FIELD_TYPES__[arg_info["Type"]],
                    "name": arg_info["Name"],
                    "notes": arg_info["Description"],
                    "values": values
                }
                ET.SubElement(node_object, "field", arg_attrs)

    # Write contents to XML
    tree = ET.ElementTree(node_root)
    ET.indent(tree, space="\t", level=0)
    print(f"Writing objectdb.xml")
    tree.write("objectdb.xml", encoding="utf-8")


if __name__ == '__main__':
    generate(database.load_database())
