import database
import os


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
           '\t\t\t<a href="classes.html">Classes</a> | \n' \
           '\t\t\t<a href="occurrences.html">Occurrences</a>\n' \
           '\t\t</header>\n' \
           '\t\t<div class="contents">\n'
EPILOGUE = '\t\t</div>\n' \
           '\t</body>\n' \
           '</html>'

# Download links
DOWNLOADS = '\t\t\t<p>\n' \
            '\t\t\t\tYou can download the latest database for Whitehole here:<br>\n' \
            '\t\t\t\t<a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.json">Whitehole Despaghettification</a><br>\n' \
            '\t\t\t\t<a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.xml">Whitehole v1.7 or older</a>\n' \
            '\t\t\t</p>\n'

# Recurring object elements and helpers
OBJECT_TABLE_HEADER = '\t\t\t<table width="100%">\n' \
                      '\t\t\t\t<tr>' \
                      '<th colspan="2">Internal Name</th>' \
                      '<th>Class Name</th>' \
                      '<th>Description</th>' \
                      '<th>Games</th>' \
                      '<th>Archive</th>' \
                      '<th>Info List</th>' \
                      '</tr>\n'

PROGRESS_TO_KEY = ["Unknown", "Known", "Finished"]
PROGRESS_TO_COLOR = ["punknown", "pknown", "pfinished"]
GAMES = ["n/a", "SMG1", "SMG2", "Both", "Custom", "SMG1, Custom", "SMG2, Custom", "Both, Custom"]


# ---------------------------------------------------------------------------------------------------------------------
# Object pages generation
# ---------------------------------------------------------------------------------------------------------------------
def pregenerate(db, object_rows, objects_by_tag, objects_by_category):
    for obj in db.objects.values():
        # Fetch object information
        name = obj["Name"]
        notes = obj["Notes"].replace("\n", "<br>")
        smg1_class_name = obj["ClassNameSMG1"]
        smg2_class_name = obj["ClassNameSMG2"]
        smg1_list_name = obj["ListSMG1"]
        smg2_list_name = obj["ListSMG2"]

        # Table row contents
        description = f'<b>{name}</b><p style="width:95%;">{notes}</p>'

        class_href = f'<a href="class_{smg1_class_name}.html">{smg1_class_name}</a>'
        if smg1_class_name != smg2_class_name:
            class_href += f'&nbsp(SMG1)<br><a href="class_{smg2_class_name}.html">{smg2_class_name}</a>&nbsp(SMG2)'

        list_name = smg1_list_name
        if smg1_list_name != smg2_list_name:
            list_name += f"&nbsp(SMG1)<br>{smg2_list_name}&nbsp(SMG2)"

        # Create the actual row
        progress_color = PROGRESS_TO_COLOR[obj["Progress"]]

        if obj["IsLeftover"]:
            unused_color = ' class="pleftover"'
        elif obj["IsUnused"]:
            unused_color = ' class="punused"'
        else:
            unused_color = ""

        row = '\t\t\t\t<tr>' \
              f'<td class="{progress_color}">&nbsp;</td>' \
              f'<td{unused_color}>{obj["InternalName"]}</td>' \
              f'<td{unused_color}>{class_href}</td>' \
              f'<td{unused_color}>{description}</td>' \
              f'<td{unused_color}>{GAMES[obj["Games"]]}</td>' \
              f'<td{unused_color}>{obj["File"]}</td>' \
              f'<td{unused_color}>{list_name}</td>' \
              '</tr>\n'

        # Sort row into appropriate lists
        object_rows.append(row)
        objects_by_tag[PROGRESS_TO_KEY[obj["Progress"]]].append(row)
        objects_by_category[obj["Category"]].append(row)

        if obj["IsUnused"]:
            objects_by_tag["Unused"].append(row)
        if obj["IsLeftover"]:
            objects_by_tag["Leftover"].append(row)


def generate_objects_overview_page(db, object_rows, objects_by_tag):
    # Begin page
    page = PROLOGUE.format("Objects Overview | Super Mario Galaxy Object Database")

    # Categories
    page += '\t\t\t<div class="tableofcontents">\n' \
            '\t\t\t\t<table>\n' \
            '\t\t\t\t\t<tr><th>Categories</th></tr>\n' \
            '\t\t\t\t\t<tr>\n' \
            '\t\t\t\t\t\t<td><ol>\n'
    for category_id, category_name in db.categories.items():
        page += f'\t\t\t\t\t\t\t<li><a href="category_{category_id}.html">{category_name}</a></li>\n'
    page += '\t\t\t\t\t\t</ol></td>\n' \
            '\t\t\t\t\t</tr>\n' \
            '\t\t\t\t</table>\n' \
            '\t\t\t</div>\n'

    # Introduction
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.\n' \
            '\t\t\t\tHere, you can find information about every object and class that can be used in the game.\n' \
            '\t\t\t\tThis page lists all objects in the <em>Galaxy</em> games. A brief description and a name\n' \
            '\t\t\t\tshould help you get an idea about what an object is used for.\n' \
            '\t\t\t</p>\n'

    # Collect object stats
    unknown_objs = len(objects_by_tag["Unknown"])
    known_objs = len(objects_by_tag["Known"])
    finished_objs = len(objects_by_tag["Finished"])
    unused_objs = len(objects_by_tag["Unused"])
    leftover_objs = len(objects_by_tag["Leftover"])
    total_objs = len(db.objects)

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


def generate_category_pages(db, objects_by_category):
    for category_id, category_name in db.categories.items():
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


def generate_tag_pages(db, objects_by_progress):
    total_objs = len(db.objects)

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
# Class pages generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_classes_overview_page(db):
    # Begin page
    page = PROLOGUE.format("Classes Overview | Super Mario Galaxy Object Database")
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.\n' \
            '\t\t\t\tHere, you can find information about every object and class that can be used in the game.\n' \
            '\t\t\t\tThis page lists all classes in the <em>Galaxy</em> games. Go to the respective pages to learn\n' \
            '\t\t\t\tmore about an individual class.\n' \
            '\t\t\t</p>\n'

    # Collect class stats
    unknown_classes = len([c for c in db.classes.values() if c["Progress"] == 0])
    known_classes = len([c for c in db.classes.values() if c["Progress"] == 1])
    finished_classes = len([c for c in db.classes.values() if c["Progress"] == 2])
    total_classes = len(db.classes)
    unknown_classes_percent = round(unknown_classes / total_classes, 4) * 100
    known_classes_percent = round(known_classes / total_classes, 4) * 100
    finished_classes_percent = round(finished_classes / total_classes, 4) * 100

    # Create the actual progress table
    page += '\t\t\t<table class="data"\n' \
            '\t\t\t\t<tr><th></th>' \
            '<th>Unknown classes</th>' \
            '<th>Known classes</th>' \
            '<th>Finished classes</th>' \
            '<th>Total classes</th>' \
            '</tr>\n' \
            f'\t\t\t\t<tr><th>Relative</th>' \
            f'<td class="punknown">{unknown_classes_percent:.2f}%</td>' \
            f'<td class="pknown">{known_classes_percent:.2f}%</td>' \
            f'<td class="pfinished">{finished_classes_percent:.2f}%</td>' \
            f'<td>100%</td>' \
            f'</tr>\n' \
            f'\t\t\t\t<tr><th>Absolute</th>' \
            f'<td class="punknown">{unknown_classes}</td>' \
            f'<td class="pknown">{known_classes}</td>' \
            f'<td class="pfinished">{finished_classes}</td>' \
            f'<td>{total_classes}</td>' \
            f'</tr>\n' \
            '\t\t\t</table>\n'

    # Add download links and begin classes table
    page += DOWNLOADS
    page += '\t\t\t<table width="100%">\n' \
            '\t\t\t\t<tr>' \
            '<th colspan="2">Class Name</th>' \
            '<th>Description</th>' \
            '<th>Games</th>' \
            '</tr>\n'

    # Write class rows
    for clazz in db.classes.values():
        class_href = f'<a href="class_{clazz["InternalName"]}.html">{clazz["InternalName"]}</a>'
        progress_color = PROGRESS_TO_COLOR[clazz["Progress"]]

        page += '\t\t\t\t<tr>' \
                f'<td class="{progress_color}">&nbsp;</td>' \
                f'<td>{class_href}</td>' \
                f'<td><p>{clazz["Notes"]}</p></td>' \
                f'<td>{GAMES[clazz["Games"]]}</td>' \
                '</tr>\n'

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/classes.html", page)


__ARGUMENTS__ = [
    "Obj_arg0", "Obj_arg1", "Obj_arg2", "Obj_arg3", "Obj_arg4", "Obj_arg5", "Obj_arg6", "Obj_arg7", "Path_arg0",
    "Path_arg1", "Path_arg2", "Path_arg3", "Path_arg4", "Path_arg5", "Path_arg6", "Path_arg7", "Point_arg0",
    "Point_arg1", "Point_arg2", "Point_arg3", "Point_arg4", "Point_arg5", "Point_arg6", "Point_arg7", "RailObj_arg0",
    "RailObj_arg1", "RailObj_arg2", "RailObj_arg3", "RailObj_arg4", "RailObj_arg5", "RailObj_arg6", "RailObj_arg7"
]
__SWITCHES__ = [
    "SW_APPEAR", "SW_DEAD", "SW_A", "SW_B", "SW_PARAM", "SW_AWAKE"
]
__SETUPS__ = [
    "Rail", "Group", "ClippingGroup", "MercatorTransform", "GeneralPos", "Message", "Camera", "DemoCast",
    "MarioFaceShipNpcRegister", "AppearPowerStar", "BaseMtxFollower", "BaseMtxFollowTarget",
]
__PROPERTIES__ = [
    "ScoreAttack", "YoshiLockOnTarget", "SearchTurtle", "MirrorActor", "DemoSimpleCast", "MoveLimitCollision",
    "MapPartsRailMover", "MapPartsRailPosture", "MapPartsRailRotator", "MapPartsRotator", "MapPartsSeesaw1AxisRotator",
    "MapPartsSeesaw2AxisRotator", "MapPartsSeesaw2AxisRollerRotator", "MapPartsFloatingForce",
    "FloaterFloatingForceTypeNormal"
]
DEFAULT_DESCS = {
    "MapPartsRailMover": "TODO",
    "MapPartsRailPosture": "TODO",
    "MapPartsRailRotator": "TODO",
    "MapPartsRotator": "TODO",
    "MapPartsSeesaw1AxisRotator": "TODO",
    "MapPartsSeesaw2AxisRotator": "TODO",
    "MapPartsSeesaw2AxisRollerRotator": "TODO",
    "MapPartsFloatingForce": "TODO",
    "FloaterFloatingForceTypeNormal": "TODO"
}


def __append_class_arguments__(actor, has_exclusives, page):
    # Declare section and header
    page += '\t\t\t<h2>Arguments</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=6%><col width=4%><col width=5%><col width=5%><col width=45%><col width=20%><col width=15%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Type</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=6%><col width=4%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Type</th><th>Games</th><th>Required?</th><th>Description</th><th>Values</th></tr>\n'

    for prop in __ARGUMENTS__:
        if prop not in actor["Parameters"]:
            continue
        info = actor["Parameters"][prop]

        description = info["Description"] if prop not in DEFAULT_DESCS else DEFAULT_DESCS[prop]
        values = "".join([f"<li>{value_info['Value']}: {value_info['Notes']}</li>" for value_info in info["Values"]])

        row = '\t\t\t\t<tr>' \
              f'<td>{prop}</td>' \
              f'<td>{info["Type"]}</td>' \
              f'<td>{GAMES[info["Games"]]}</td>' \
              f'<td>{info["Needed"]}</td>' \
              f'<td><p><b>{info["Name"]}</b>: {description}</p></td>' \
              f'<td><ul>{values}</ul></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # Wrap up section
    page += '\t\t\t</table>\n'
    return page


def __append_class_switches__(actor, has_exclusives, page):
    # Declare section and header
    page += '\t\t\t<h2>Switches</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=80%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th></tr>\n'

    for prop in __SWITCHES__:
        if prop not in actor["Parameters"]:
            continue
        info = actor["Parameters"][prop]

        # Write switch row
        description = info["Description"] if prop not in DEFAULT_DESCS else DEFAULT_DESCS[prop]

        row = '\t\t\t\t<tr>' \
              f'<td>{prop}</td>' \
              f'<td>{GAMES[info["Games"]]}</td>' \
              f'<td>{info.get("Needed", False)}</td>' \
              f'<td><p>{description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def __append_class_setups__(actor, has_exclusives, page):
    # Declare section and header
    page += '\t\t\t<h2>Setup</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=80%></colgroup>\n' \
                '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th></tr>\n'

    for prop in __SETUPS__:
        if prop not in actor["Parameters"]:
            continue
        info = actor["Parameters"][prop]

        # Write property row
        description = info["Description"] if prop not in DEFAULT_DESCS else DEFAULT_DESCS[prop]

        row = '\t\t\t\t<tr>' \
              f'<td>{prop}</td>' \
              f'<td>{GAMES[info["Games"]]}</td>' \
              f'<td>{info.get("Needed", False)}</td>' \
              f'<td><p>{description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def __append_class_properties__(actor, has_exclusives, page):
    # Declare section and header
    page += '\t\t\t<h2>Properties</h2>\n' \
            '\t\t\t<table width="100%">\n'

    if has_exclusives:
        page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Description</th><th>Exclusives?</th></tr>\n'
    else:
        page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Description</th></tr>\n'

    for prop in __PROPERTIES__:
        if prop not in actor["Parameters"]:
            continue
        info = actor["Parameters"][prop]

        # Write property row
        description = info["Description"] if prop not in DEFAULT_DESCS else DEFAULT_DESCS[prop]

        row = '\t\t\t\t<tr>' \
              f'<td>{prop}</td>' \
              f'<td>{GAMES[info["Games"]]}</td>' \
              f'<td><p>{description}</p></td>'
        if has_exclusives:
            exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])
            row += f'<td><ul>{exclusives}</ul></td>'
        row += '</tr>\n'

        page += row

    # End section
    page += '\t\t\t</table>\n'
    return page


def generate_class_pages(db):
    for key, actor in db.classes.items():
        # Begin page
        page = PROLOGUE.format(f'Class: {actor["InternalName"]} -- Super Mario Galaxy Object Database')
        page += f'\t\t\t<h1>Class: {actor["InternalName"]}</h1>\n' \
                f'\t\t\t<p>{actor["Notes"]}</p>\n'

        # Determine what parameter categories to populate
        def preprocess_property_category(container):
            support_category = False
            support_exclusives = False

            for prop in container:
                if support_exclusives:
                    break

                if prop in actor["Parameters"]:
                    support_category = True

                    if len(actor["Parameters"][prop]["Exclusives"]) > 0:
                        support_exclusives = True

            return support_category, support_exclusives

        has_arguments, has_exclusives_arguments = preprocess_property_category(__ARGUMENTS__)
        has_switches, has_exclusives_switches = preprocess_property_category(__SWITCHES__)
        has_setups, has_exclusives_setups = preprocess_property_category(__SETUPS__)
        has_properties, has_exclusives_properties = preprocess_property_category(__PROPERTIES__)

        if has_arguments:
            page = __append_class_arguments__(actor, has_exclusives_arguments, page)
        if has_switches:
            page = __append_class_switches__(actor, has_exclusives_switches, page)
        if has_setups:
            page = __append_class_setups__(actor, has_exclusives_switches, page)
        if has_properties:
            page = __append_class_properties__(actor, has_exclusives_properties, page)

        # Wrap up page
        page += EPILOGUE
        write_strings_file(f'docs/class_{key}.html', page)


# ---------------------------------------------------------------------------------------------------------------------
# Occurrence pages generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_occurrence_overview_page(db):
    # Begin page
    page = PROLOGUE.format(f'Object Occurrences -- Super Mario Galaxy Object Database')
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.\n' \
            '\t\t\t\tHere, you can find information about every object and class that can be used in the game.\n' \
            '\t\t\t\tThis page lists all object occurrences in the <em>Galaxy</em> games. Go to the respective\n' \
            '\t\t\t\tpages to view the detailed object dumps.\n' \
            '\t\t\t</p>\n' \
            '\t\t\t<table>\n' \
            '\t\t\t\t<tr><th>Object</th><th>Unique Occurrences</th></tr>\n'

    # Write occurrence overview rows
    for obj_name, occurrences in db.occurrences.items():
        url = f'<a href="occurrences_{obj_name}.html">{obj_name}</a>'
        page += f'\t\t\t\t<tr><td>{url}</td><td>{len(occurrences)}</td></tr>\n'

    # Wrap up page
    page += '\t\t\t</table>\n'
    page += EPILOGUE
    write_strings_file(f'docs/occurrences.html', page)


def generate_occurrence_pages(db):
    for obj_name, occurrences in db.occurrences.items():
        # Begin page
        page = PROLOGUE.format(f'Occurrences: {obj_name} -- Super Mario Galaxy Object Database')
        page += f'\t\t\t<h1>Occurrences: {obj_name}</h1>\n' \
                f'\t\t\t<table>'

        # Collect columns
        column_names = list()

        for entry in occurrences:
            for column in entry.keys():
                if column not in column_names:
                    column_names.append(column)

        column_names.sort(key=database.FIELD_COLUMN_ORDER)

        # Write header
        header = "</th><th>".join(column_names)
        page += f'\t\t\t\t<tr><th>{header}</th></tr>\n'

        # Write actual entries
        for occurrence in occurrences:
            row = "\t\t\t\t<tr>"
            for column in column_names:
                value = str(occurrence[column] if column in occurrence else database.default_field_value(column))
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
def generate(db, do_occurrences: bool):
    # Prepare data holders
    objects_by_tag = {"Unknown": list(), "Known": list(), "Finished": list(), "Unused": list(), "Leftover": list()}
    objects_by_category = {c: list() for c in db.categories.keys()}
    object_rows = list()

    # Generate the actual contents
    pregenerate(db, object_rows, objects_by_tag, objects_by_category)
    generate_objects_overview_page(db, object_rows, objects_by_tag)
    generate_category_pages(db, objects_by_category)
    generate_tag_pages(db, objects_by_tag)

    generate_classes_overview_page(db)
    generate_class_pages(db)

    if do_occurrences:
        generate_occurrence_overview_page(db)
        generate_occurrence_pages(db)


if __name__ == '__main__':
    db = database.load_database()
    generate(db, True)
