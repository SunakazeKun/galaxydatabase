import database
import os

from database import GalaxyDatabase, GalaxyObject, GalaxyConfig, GalaxyConfigProperty


# ---------------------------------------------------------------------------------------------------------------------
# Prepare page templates
# ---------------------------------------------------------------------------------------------------------------------
# File writer
def write_strings_file(file_path: str, strings):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(strings)
        f.flush()


# Page prologue and epiloque
PROLOGUE = '<!DOCTYPE html>\n' \
           '<html>\n' \
           '\t<head>\n' \
           '\t\t<title>{0:s}</title>\n' \
           '\t\t<link rel="shortcut icon" type="image/x-icon" href="icon.png">\n' \
           '\t\t<link rel="stylesheet" href="normalize.css">\n' \
           '\t\t<link rel="stylesheet" href="style.css">\n' \
           '\t\t<meta name="keywords" content="Super,Mario,Galaxy,Object,Database,Documentation">\n' \
           '\t\t<meta name="description" content="Super Mario Galaxy Object Database">\n' \
           '\t\t<meta charset="UTF-8">\n' \
           '\t</head>\n' \
           '\t<body>\n' \
           '\t\t<header>\n' \
           '\t\t\t<h1>Super Mario Galaxy Object Database</h1>\n' \
           '\t\t\t<a href="index.html">Objects</a> | \n' \
           '\t\t\t<a href="configs.html">Configs</a> | \n' \
           '\t\t\t<a href="occurrences.html">Occurrences</a>\n' \
           '\t\t</header>\n' \
           '\t\t<div class="contents">\n'
EPILOGUE = '\t\t</div>\n' \
           '\t</body>\n' \
           '</html>'

# Download links
DOWNLOADS = '\t\t\t<p>\n' \
            '\t\t\t\tYou can download the latest database for Whitehole here:<br>\n' \
            '\t\t\t\t<a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.json" download>Whitehole Despaghettification</a><br>\n' \
            '\t\t\t\t<a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.xml" download>Whitehole v1.7 or older</a>\n' \
            '\t\t\t</p>\n'

# Recurring object elements and helpers
OBJECT_TABLE_HEADER = '\t\t\t<table width="100%">\n' \
                      '\t\t\t\t<tr>' \
                      '<th colspan="2">Internal name</th>' \
                      '<th>Config name</th>' \
                      '<th>Description</th>' \
                      '<th>Games</th>' \
                      '<th>Archive</th>' \
                      '<th>Info list</th>' \
                      '</tr>\n'

PROGRESS_TO_KEY = ["Unknown", "Known", "Finished"]
PROGRESS_TO_COLOR = ["punknown", "pknown", "pfinished"]
GAMES = ["n/a", "SMG1", "SMG2", "Both", "Custom", "SMG1, Custom", "SMG2, Custom", "Both, Custom"]


# ---------------------------------------------------------------------------------------------------------------------
# Object pages generation
# ---------------------------------------------------------------------------------------------------------------------
def pregenerate(galaxy_db: GalaxyDatabase, object_rows: list[str], objects_by_tag: dict[str, list[str]],
                objects_by_category: dict[str, list[str]]):
    for obj in galaxy_db.objects.values():
        # Fetch object information
        name = obj.name
        notes = obj.notes.replace("\n", "<br>")
        smg1_config_name = obj.config_name_smg1
        smg2_config_name = obj.config_name_smg2
        smg1_list_name = obj.list_smg1
        smg2_list_name = obj.list_smg2

        # Table row contents
        description = f'<b>{name}</b><p style="width:95%;">{notes}</p>'

        config_href = f'<a href="config_{smg1_config_name}.html">{smg1_config_name}</a>'
        if smg1_config_name != smg2_config_name:
            config_href += f'&nbsp(SMG1)<br><a href="config_{smg2_config_name}.html">{smg2_config_name}</a>&nbsp(SMG2)'

        list_name = smg1_list_name
        if smg1_list_name != smg2_list_name:
            list_name += f"&nbsp(SMG1)<br>{smg2_list_name}&nbsp(SMG2)"

        # Create the actual row
        progress_color = PROGRESS_TO_COLOR[obj.progress]

        if obj.is_leftover:
            unused_color = ' class="pleftover"'
        elif obj.is_unused:
            unused_color = ' class="punused"'
        else:
            unused_color = ""

        row = '\t\t\t\t<tr>' \
              f'<td class="{progress_color}">&nbsp;</td>' \
              f'<td{unused_color}>{obj.internal_name}</td>' \
              f'<td{unused_color}>{config_href}</td>' \
              f'<td{unused_color}>{description}</td>' \
              f'<td{unused_color}>{GAMES[obj.games]}</td>' \
              f'<td{unused_color}>{obj.file}</td>' \
              f'<td{unused_color}>{list_name}</td>' \
              '</tr>\n'

        # Sort row into appropriate lists
        object_rows.append(row)
        objects_by_tag[PROGRESS_TO_KEY[obj.progress]].append(row)
        objects_by_category[obj.category].append(row)

        if obj.is_unused:
            objects_by_tag["Unused"].append(row)
        if obj.is_leftover:
            objects_by_tag["Leftover"].append(row)


def generate_objects_overview_page(galaxy_db: GalaxyDatabase, object_rows: list[str],
                                   objects_by_tag: dict[str, list[str]]):
    # Begin page
    page = PROLOGUE.format("Objects Overview | Super Mario Galaxy Object Database")

    # Categories
    page += '\t\t\t<div class="tableofcontents">\n' \
            '\t\t\t\t<table>\n' \
            '\t\t\t\t\t<tr><th>Categories</th></tr>\n' \
            '\t\t\t\t\t<tr>\n' \
            '\t\t\t\t\t\t<td><ol>\n'
    for category_id, category_name in galaxy_db.categories.items():
        page += f'\t\t\t\t\t\t\t<li><a href="category_{category_id}.html">{category_name}</a></li>\n'
    page += '\t\t\t\t\t\t</ol></td>\n' \
            '\t\t\t\t\t</tr>\n' \
            '\t\t\t\t</table>\n' \
            '\t\t\t</div>\n'

    # Introduction
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.</br>\n' \
            '\t\t\t\t<br>\n' \
            '\t\t\t\tOn this page you can find information about every object in the <em>Galaxy</em> games. A brief\n' \
            '\t\t\t\tdescription and a name should help you get an idea about what an object is used for. Detailed' \
            '\t\t\t\tinformation such as <em>Obj_arg</em> settings can be found on the respective config pages.\n' \
            '\t\t\t</p>\n'

    # Collect object stats
    unknown_objs = len(objects_by_tag["Unknown"])
    known_objs = len(objects_by_tag["Known"])
    finished_objs = len(objects_by_tag["Finished"])
    unused_objs = len(objects_by_tag["Unused"])
    leftover_objs = len(objects_by_tag["Leftover"])
    total_objs = len(galaxy_db.objects)

    unknown_objs_percent = round(unknown_objs / total_objs, 4) * 100
    known_objs_percent = round(known_objs / total_objs, 4) * 100
    finished_objs_percent = round(finished_objs / total_objs, 4) * 100
    unused_objs_percent = round(unused_objs / total_objs, 4) * 100
    leftover_objs_percent = round(leftover_objs / total_objs, 4) * 100

    # Create tag links
    def create_href(count, tag):
        if count == 0 or count == total_objs:
            return tag + " objects"
        return f'<a href="tag_{tag}.html">{tag} objects</a>'

    unknown_href = create_href(unknown_objs, "Unknown")
    known_href = create_href(known_objs, "Known")
    finished_href = create_href(finished_objs, "Finished")
    unused_href = create_href(unused_objs, "Unused")
    leftover_href = create_href(leftover_objs, "Leftover")

    # Create the actual progress table
    page += '\t\t\t<table class="data"\n' \
            '\t\t\t\t<tr><th></th>' \
            f'<th>{unknown_href}</th>' \
            f'<th>{known_href}</th>' \
            f'<th>{finished_href}</th>' \
            f'<th>{unused_href}</th>' \
            f'<th>{leftover_href}</th>' \
            '<th>Total objects</th>' \
            '</tr>\n' \
            '\t\t\t\t<tr><th>Relative</th>' \
            f'<td class="punknown">{unknown_objs_percent:.2f}%</td>' \
            f'<td class="pknown">{known_objs_percent:.2f}%</td>' \
            f'<td class="pfinished">{finished_objs_percent:.2f}%</td>' \
            f'<td class="punused">{unused_objs_percent:.2f}%</td>' \
            f'<td class="pleftover">{leftover_objs_percent:.2f}%</td>' \
            '<td>100%</td>' \
            '</tr>\n' \
            '\t\t\t\t<tr><th>Absolute</th>' \
            f'<td class="punknown">{unknown_objs}</td>' \
            f'<td class="pknown">{known_objs}</td>' \
            f'<td class="pfinished">{finished_objs}</td>' \
            f'<td class="punused">{unused_objs}</td>' \
            f'<td class="pleftover">{leftover_objs}</td>' \
            f'<td>{total_objs}</td>' \
            '</tr>\n' \
            '\t\t\t</table>\n'

    # Add download links and begin objects table
    page += DOWNLOADS
    page += OBJECT_TABLE_HEADER

    # Write object rows
    for row in object_rows:
        page += row

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/index.html", page)


def generate_category_pages(galaxy_db: GalaxyDatabase, objects_by_category: dict[str, list[str]]):
    for category_id, category_name in galaxy_db.categories.items():
        # Begin page
        page = PROLOGUE.format(f"Category: {category_name} | Super Mario Galaxy Object Database")
        page += f'\t\t\t<h1>Category: {category_name}</h1>\n'
        page += OBJECT_TABLE_HEADER

        # Write table rows
        for row in objects_by_category[category_id]:
            page += row

        # Wrap up table and page
        page += "\t\t\t</table>\n"
        page += EPILOGUE
        write_strings_file(f"docs/category_{category_id}.html", page)


def generate_progress_pages(galaxy_db: GalaxyDatabase, objects_by_progress: dict[str, list[str]]):
    total_objs = len(galaxy_db.objects)

    for tag_name, tag_rows in objects_by_progress.items():
        if len(tag_rows) == 0 or len(tag_rows) == total_objs:
            continue

        # Begin page
        page = PROLOGUE.format(f"{tag_name} objects | Super Mario Galaxy Object Database")
        page += f'\t\t\t<h1>{tag_name} objects</h1>\n'
        page += OBJECT_TABLE_HEADER

        # Write table rows
        for row in tag_rows:
            page += row

        # Wrap up table and page
        page += "\t\t\t</table>\n"
        page += EPILOGUE
        write_strings_file(f"docs/tag_{tag_name}.html", page)


# ---------------------------------------------------------------------------------------------------------------------
# Config pages generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_configs_overview_page(db):
    # Begin page
    page = PROLOGUE.format("Configs Overview | Super Mario Galaxy Object Database")
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.<br>\n' \
            '\t\t\t\t<br>\n' \
            '\t\t\t\tThis page lists all configs in the <em>Galaxy</em> games. Go to the respective pages to learn\n' \
            '\t\t\t\tmore about an individual object config.\n' \
            '\t\t\t</p>\n'

    # Collect config stats
    unknown_configs = len([c for c in db.configs.values() if c.progress == 0])
    known_configs = len([c for c in db.configs.values() if c.progress == 1])
    finished_configs = len([c for c in db.configs.values() if c.progress == 2])
    total_configs = len(db.configs)
    unknown_configs_percent = round(unknown_configs / total_configs, 4) * 100
    known_configs_percent = round(known_configs / total_configs, 4) * 100
    finished_configs_percent = round(finished_configs / total_configs, 4) * 100

    # Create the actual progress table
    page += '\t\t\t<table class="data"\n' \
            '\t\t\t\t<tr><th></th>' \
            '<th>Unknown configs</th>' \
            '<th>Known configs</th>' \
            '<th>Finished configs</th>' \
            '<th>Total configs</th>' \
            '</tr>\n' \
            f'\t\t\t\t<tr><th>Relative</th>' \
            f'<td class="punknown">{unknown_configs_percent:.2f}%</td>' \
            f'<td class="pknown">{known_configs_percent:.2f}%</td>' \
            f'<td class="pfinished">{finished_configs_percent:.2f}%</td>' \
            f'<td>100%</td>' \
            f'</tr>\n' \
            f'\t\t\t\t<tr><th>Absolute</th>' \
            f'<td class="punknown">{unknown_configs}</td>' \
            f'<td class="pknown">{known_configs}</td>' \
            f'<td class="pfinished">{finished_configs}</td>' \
            f'<td>{total_configs}</td>' \
            f'</tr>\n' \
            '\t\t\t</table>\n'

    # Add download links and begin configs table
    page += DOWNLOADS
    page += '\t\t\t<table width="100%">\n' \
            '\t\t\t\t<tr>' \
            '<th colspan="2">Config name</th>' \
            '<th>Description</th>' \
            '<th>Games</th>' \
            '</tr>\n'

    # Write class rows
    for galaxy_config in db.configs.values():
        class_href = f'<a href="config_{galaxy_config.internal_name}.html">{galaxy_config.internal_name}</a>'
        progress_color = PROGRESS_TO_COLOR[galaxy_config.progress]

        page += '\t\t\t\t<tr>' \
                f'<td class="{progress_color}">&nbsp;</td>' \
                f'<td>{class_href}</td>' \
                f'<td><p><b>{galaxy_config.name}</b>:</p><p>{galaxy_config.notes}</p></td>' \
                f'<td>{GAMES[galaxy_config.games]}</td>' \
                '</tr>\n'

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/configs.html", page)


def __append_config_arguments__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>Arguments</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=6%><col width=4%><col width=5%><col width=5%><col width=45%><col width=20%><col width=15%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Type</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=6%><col width=4%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Type</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th></tr>\n'

    for config_property in properties:
        values = "".join([f"<li>{val_info['Value']}: {val_info['Notes']}</li>" for val_info in config_property.values])

        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{config_property.type}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td>{config_property.needed}</td>' \
              f'<td><p><b>{config_property.name}</b>: {config_property.description}</p></td>' \
              f'<td><ul>{values}</ul></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # Wrap up section
    page += '\t\t\t</table>\n'
    return page


def __append_config_mapparts_arguments__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>MapParts arguments</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=45%><col width=20%><col width=15%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th></tr>\n'

    for config_property in properties:
        values = "".join([f"<li>{val_info['Value']}: {val_info['Notes']}</li>" for val_info in config_property.values])

        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td>{config_property.needed}</td>' \
              f'<td><p><b>{config_property.name}</b>: {config_property.description}</p></td>' \
              f'<td><ul>{values}</ul></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # Wrap up section
    page += '\t\t\t</table>\n'
    return page


def __append_config_switches__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>Switches</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=80%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th></tr>\n'

    for config_property in properties:
        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td>{config_property.needed}</td>' \
              f'<td><p>{config_property.description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def __append_config_talking__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>Talking</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=6%><col width=5%><col width=5%><col width=45%><col width=24%><col width=15%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=6%><col width=5%><col width=5%><col width=50%><col width=34%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th></tr>\n'

    for config_property in properties:
        values = "".join([f"<li>{val_info['Value']}: {val_info['Notes']}</li>" for val_info in config_property.values])

        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td>{config_property.needed}</td>' \
              f'<td><p>{config_property.description}</p></td>' \
              f'<td><ul>{values}</ul></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def __append_config_setups__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>Setup</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=80%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th></tr>\n'

    for config_property in properties:
        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td>{config_property.needed}</td>' \
              f'<td><p>{config_property.description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def __append_config_properties__(properties: list[GalaxyConfigProperty], has_exclusives: bool, page: str) -> str:
    # Declare section and header
    page += '\t\t\t<h2>Properties</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Description</th></tr>\n'

    for config_property in properties:
        row = '\t\t\t\t<tr>' \
              f'<td>{config_property.identifier}</td>' \
              f'<td>{GAMES[config_property.games]}</td>' \
              f'<td><p>{config_property.description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{exclusive}</li>" for exclusive in config_property.exclusives])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def generate_config_pages(galaxy_db: GalaxyDatabase):
    for config_id, galaxy_config in galaxy_db.configs.items():
        # Begin page
        page = PROLOGUE.format(f'Config: {galaxy_config.name} -- Super Mario Galaxy Object Database')
        page += f'\t\t\t<h1>Config: {galaxy_config.name}</h1>\n' \
                f'\t\t\t<p>{galaxy_config.notes}</p>\n'

        # Preprocess properties to find out what property categories should be displayed
        property_category_checks = {
            "arg": [[], False],
            "mapparts_arg": [[], False],
            "switch": [[], False],
            "setup": [[], False],
            "talking": [[], False],
            "property": [[], False]
        }

        for property_id, config_property in galaxy_config.properties.items():
            property_category = database.get_property_info(property_id).category_name
            property_category_checks[property_category][0].append(config_property)

            if len(config_property.exclusives) > 0:
                property_category_checks[property_category][1] = True

        args, has_exclusive_args = property_category_checks["arg"]
        mapparts_args, has_exclusive_mapparts_args = property_category_checks["mapparts_arg"]
        switches, has_exclusive_switches = property_category_checks["switch"]
        talking, has_exclusive_talking = property_category_checks["talking"]
        setups, has_exclusive_setups = property_category_checks["setup"]
        properties, has_exclusive_properties = property_category_checks["property"]

        if len(args) > 0:
            page = __append_config_arguments__(args, has_exclusive_args, page)
        if len(mapparts_args) > 0:
            page = __append_config_mapparts_arguments__(mapparts_args, has_exclusive_args, page)
        if len(switches) > 0:
            page = __append_config_switches__(switches, has_exclusive_switches, page)
        if len(talking) > 0:
            page = __append_config_talking__(talking, has_exclusive_talking, page)
        if len(setups) > 0:
            page = __append_config_setups__(setups, has_exclusive_setups, page)
        if len(properties) > 0:
            page = __append_config_properties__(properties, has_exclusive_properties, page)

        # Wrap up page
        page += EPILOGUE
        write_strings_file(f'docs/config_{config_id}.html', page)


# ---------------------------------------------------------------------------------------------------------------------
# Occurrence pages generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_occurrence_overview_page(galaxy_db: GalaxyDatabase):
    # Begin page
    page = PROLOGUE.format(f'Object occurrences -- Super Mario Galaxy Object Database')
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.<br>\n' \
            '\t\t\t\t<br>\n' \
            '\t\t\t\tThis page lists all object occurrences in the <em>Galaxy</em> games. Go to the respective\n' \
            '\t\t\t\tpages to view the detailed object dumps.\n' \
            '\t\t\t</p>\n' \
            '\t\t\t<table>\n' \
            '\t\t\t\t<tr><th>Object</th><th>Unique occurrences</th></tr>\n'

    # Write occurrence overview rows
    for obj_name, occurrences in galaxy_db.occurrences.items():
        url = f'<a href="occurrences_{obj_name}.html">{obj_name}</a>'
        page += f'\t\t\t\t<tr><td>{url}</td><td>{len(occurrences)}</td></tr>\n'

    # Wrap up page
    page += '\t\t\t</table>\n'
    page += EPILOGUE
    write_strings_file('docs/occurrences.html', page)


def generate_occurrence_pages(galaxy_db: GalaxyDatabase):
    for obj_name, occurrences in galaxy_db.occurrences.items():
        # Begin page
        page = PROLOGUE.format(f'Occurrences: {obj_name} -- Super Mario Galaxy Object Database')
        page += f'\t\t\t<h1>Occurrences: {obj_name}</h1>\n' \
                f'\t\t\t<table>'

        # Collect columns
        column_names = list()

        for occurrence in occurrences:
            for column in occurrence.keys():
                if column not in column_names:
                    column_names.append(column)

        column_names.sort(key=database.occurrence_field_order_key())

        # Write header
        header = "</th><th>".join(column_names)
        page += f'\t\t\t\t<tr><th>{header}</th></tr>\n'

        # Write actual entries
        for occurrence in occurrences:
            row = "\t\t\t\t<tr>"

            for column in column_names:
                if column in occurrence:
                    value = str(occurrence[column])
                else:
                    value = str(database.default_occurrence_field_value(column))
                row += f'<td>{value}</td>'

            row += "</tr>\n"
            page += row

        # Wrap up page
        page += '\t\t\t</table>\n'
        page += EPILOGUE
        write_strings_file(f'docs/occurrences_{obj_name}.html', page)


# ---------------------------------------------------------------------------------------------------------------------
# Generation Sequence and Entry Point
# ---------------------------------------------------------------------------------------------------------------------
def generate_docs(galaxy_db: GalaxyDatabase, do_occurrences: bool):
    # Prepare data holders
    objects_by_tag = {"Unknown": list(), "Known": list(), "Finished": list(), "Unused": list(), "Leftover": list()}
    objects_by_category = {c: list() for c in galaxy_db.categories.keys()}
    object_rows = []

    # Generate the actual contents
    pregenerate(galaxy_db, object_rows, objects_by_tag, objects_by_category)
    generate_objects_overview_page(galaxy_db, object_rows, objects_by_tag)
    generate_category_pages(galaxy_db, objects_by_category)
    generate_progress_pages(galaxy_db, objects_by_tag)

    generate_configs_overview_page(galaxy_db)
    generate_config_pages(galaxy_db)

    if do_occurrences:
        generate_occurrence_overview_page(galaxy_db)
        generate_occurrence_pages(galaxy_db)


if __name__ == '__main__':
    generate_docs(database.load_database(), True)
