from database import GalaxyDatabase, GalaxyObject, GalaxyConfig, GalaxyConfigProperty

import database
import datetime
import math
import xml.etree.ElementTree as ET

__FIELD_TYPES__ = {"Integer": "int", "Bitfield": "int", "Float": "float", "Boolean": "bool"}


def generate_whitehole_xml(galaxy_db: GalaxyDatabase):
    # Create "database" root element
    timestamp = math.floor(datetime.datetime.now().timestamp())
    root_node = ET.Element("database")
    root_node.set("timestamp", str(timestamp))

    # Create category elements
    category_indices = dict()
    node_categories = ET.SubElement(root_node, "categories")

    for i, (category_key, category_desc) in enumerate(galaxy_db.categories.items()):
        category_indices[category_key] = i
        ET.SubElement(node_categories, "category", {"id": str(i)}).text = category_desc

    # Create object elements. Whitehole 1.7 and earlier do not differentiate between objects and actors
    for obj_key in galaxy_db.objects.keys():
        galaxy_object: GalaxyObject = galaxy_db.objects[obj_key]
        galaxy_config: GalaxyConfig = galaxy_db.configs.get(galaxy_object.config_name_smg2, None)
        properties: dict[str, GalaxyConfigProperty] = galaxy_config.properties if galaxy_config is not None else {}

        # Collect node information
        flags = {
            "games": str(galaxy_object.games),
            "known": str(int(galaxy_object.progress >= 1)),
            "complete": str(int(galaxy_object.progress >= 2)),
            "needsPaths": "1" if "Rail" in properties and properties["Rail"].needed else "0"
        }

        object_notes = galaxy_object.notes
        config_notes = "" if galaxy_config is None else galaxy_config.notes
        category_id = str(category_indices[galaxy_object.category])
        preferred_file = galaxy_object.list_smg2.replace("Info", "")
        notes = f'-- OBJECT NOTES --\n{object_notes}\n\n-- CLASS NOTES --\n{config_notes}'

        # Create object node
        object_node = ET.SubElement(root_node, "object", {"id": galaxy_object.internal_name})
        ET.SubElement(object_node, "name").text = galaxy_object.name
        ET.SubElement(object_node, "flags", flags)
        ET.SubElement(object_node, "category", {"id": category_id})
        ET.SubElement(object_node, "preferredfile", {"name": preferred_file})
        ET.SubElement(object_node, "notes").text = notes
        ET.SubElement(object_node, "files")  # UseResource stuff is not part of this DB's scope

        # Append Obj_args
        if len(properties) == 0:
            continue

        for i in range(8):
            arg_name = f"Obj_arg{i}"

            if arg_name in galaxy_config.properties:
                arg_info = galaxy_config.properties[arg_name]

                # Only append to objects that support this field
                if len(arg_info.exclusives) and obj_key not in arg_info.exclusives:
                    continue

                values = ", ".join([f"{l['Value']} = {l['Notes']}" for l in arg_info.values])

                arg_attrs = {
                    "id": str(i),
                    "type": __FIELD_TYPES__[arg_info.type],
                    "name": arg_info.name,
                    "notes": arg_info.description,
                    "values": values
                }
                ET.SubElement(object_node, "field", arg_attrs)

    # Write contents to XML
    tree = ET.ElementTree(root_node)
    ET.indent(tree, space="\t", level=0)
    print("Writing objectdb.xml")
    tree.write("objectdb.xml", encoding="utf-8")


if __name__ == '__main__':
    generate_whitehole_xml(database2.load_database())
