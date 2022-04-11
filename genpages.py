import database
import os


# ---------------------------------------------------------------------------------------------------------------------
# Prepare page templates
# ---------------------------------------------------------------------------------------------------------------------
# File writer
def write_strings_file(file_path: str, strings):
    dirpath = os.path.dirname(file_path)
    os.makedirs(dirpath, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(strings)
        f.flush()


# Declare page prologue and epilogue
PROLOGUE = '<!DOCTYPE html>\n' \
           '<html>\n' \
           '	<head>\n' \
           '		<title>{0:s}</title>\n' \
           '		<link rel="shortcut icon" type="image/x-icon" href="icon.png">\n' \
           '		<link rel="stylesheet" href="normalize.css">\n' \
           '		<link rel="stylesheet" href="style.css">\n' \
           '		<meta name="keywords" content="Super,Mario,Galaxy,Object,Database,Documentation">\n' \
           '		<meta name="description" content="Super Mario Galaxy Object Database">\n' \
           '		<meta charset="UTF-8">\n' \
           '	</head>\n' \
           '	<body>\n' \
           '		<header>\n' \
           '			<h1>Super Mario Galaxy Object Database</h1>\n' \
           '			<a href="index.html">Objects</a> | \n' \
           '			<a href="classes.html">Classes</a>\n' \
           '		</header>\n' \
           '		<div class="contents">\n'
EPILOGUE = '		</div>\n' \
           '	</body>\n' \
           '</html>'
# Downloads
DOWNLOADS = '\t\t\t<p><a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.xml" download>' \
            'You can also download the latest database for Whitehole here.</a></p>\n'
# Table data helpers
PROGRESS_TO_COLOR = ["punknown", "pknown", "pfinished"]
GAMES = ["n/a", "SMG1", "SMG2", "Both"]


# ---------------------------------------------------------------------------------------------------------------------
# Objects Overview and Index Page Generation
# ---------------------------------------------------------------------------------------------------------------------
def pregenerate(db, objects_by_progress, objects_by_list, objects_by_category):
    for obj in db.objects.values():
        class_href = f'<a href="class_{obj["ClassName"]}.html">{obj["ClassName"]}</a>'
        description = f'<details><summary>{obj["Name"]}</summary><p>{obj["Notes"]}</p></details>'
        list_name = db.classes[obj["ClassName"]]["List"]
        file_name = db.classes[obj["ClassName"]]["File"]
        games = GAMES[obj["Games"]]

        progress_color = PROGRESS_TO_COLOR[obj["Progress"]]
        unused_color = ' class="punused"' if obj["IsUnused"] else ""

        row = '\t\t\t\t<tr>' \
              f'<td class="{progress_color}">&nbsp;</td>' \
              f'<td{unused_color}>{obj["InternalName"]}</td>' \
              f'<td{unused_color}>{class_href}</td>' \
              f'<td{unused_color}>{description}</td>' \
              f'<td{unused_color}>{games}</td>' \
              f'<td{unused_color}>{file_name}</td>' \
              '</tr>\n'

        # Sort row into appropriate lists
        objects_by_list[list_name].append(row)
        objects_by_category[obj["Category"]].append(row)

        if obj["IsUnused"]:
            objects_by_progress["Unused"].append(row)
        if obj["IsLeftover"]:
            objects_by_progress["Leftover"].append(row)

        if obj["Progress"] == 0:
            objects_by_progress["Unknown"].append(row)
        elif obj["Progress"] == 1:
            objects_by_progress["Known"].append(row)
        elif obj["Progress"] == 2:
            objects_by_progress["Finished"].append(row)


def generate_objects_overview_page(db, objects_by_progress, objects_by_list):
    page = PROLOGUE.format("Objects Overview | Super Mario Galaxy Object Database")

    # Table of contents
    page += '\t\t\t<div class="tableofcontents">\n' \
            '\t\t\t\t<table>\n' \
            '\t\t\t\t\t<tr><th>Contents</th><th>Categories</th></tr>\n' \
            '\t\t\t\t\t<tr>\n' \
            '\t\t\t\t\t\t<td><ol>\n'
    for obj_list in db.lists:
        # We don't need GeneralPosInfo lol
        if obj_list == "GeneralPosInfo":
            continue
        page += f'\t\t\t\t\t\t\t<li><a href="#{obj_list.lower()}">{obj_list}</a></li>\n'
    page += '\t\t\t\t\t\t</ol></td>\n' \
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

    # Progress table
    unknown_objs = len(objects_by_progress["Unknown"])
    known_objs = len(objects_by_progress["Known"])
    finished_objs = len(objects_by_progress["Finished"])
    unused_objs = len(objects_by_progress["Unused"])
    total_objs = len(db.objects)
    unknown_objs_percent = round(unknown_objs / total_objs, 4) * 100
    known_objs_percent = round(known_objs / total_objs, 4) * 100
    finished_objs_percent = round(finished_objs / total_objs, 4) * 100
    unused_objs_percent = round(unused_objs / total_objs, 4) * 100

    page += '\t\t\t<table class="data"\n' \
            '\t\t\t\t<tr><th></th>' \
            '<th><a href="tag_Unknown.html">Unknown objects</a></th>' \
            '<th><a href="tag_Known.html">Known objects</a></th>' \
            '<th><a href="tag_Finished.html">Finished objects</a></th>' \
            '<th><a href="tag_Unused.html">Unused objects</a></th>' \
            '<th>Total objects</th>' \
            '</tr>\n' \
            f'\t\t\t\t<tr><th>Relative</th>' \
            f'<td class="punknown">{unknown_objs_percent:.2f}%</td>' \
            f'<td class="pknown">{known_objs_percent:.2f}%</td>' \
            f'<td class="pfinished">{finished_objs_percent:.2f}%</td>' \
            f'<td class="punused">{unused_objs_percent:.2f}%</td>' \
            f'<td>100%</td>' \
            f'</tr>\n' \
            f'\t\t\t\t<tr><th>Absolute</th>' \
            f'<td class="punknown">{unknown_objs}</td>' \
            f'<td class="pknown">{known_objs}</td>' \
            f'<td class="pfinished">{finished_objs}</td>' \
            f'<td class="punused">{unused_objs}</td>' \
            f'<td>{total_objs}</td>' \
            f'</tr>\n' \
            '\t\t\t</table>\n'

    page += DOWNLOADS

    #  Begin table
    page += '\t\t\t<table width="100%">\n' \
            '\t\t\t\t<tr>' \
            '<th colspan="2">Internal Name</th>' \
            '<th>Class Name</th>' \
            '<th>Description</th>' \
            '<th>Games</th>' \
            '<th>Archive</th>' \
            '</tr>\n'

    # Write object rows
    for obj_list, rows in objects_by_list.items():
        if obj_list == "GeneralPosInfo":
            continue

        page += f'\t\t\t\t<tr id="{obj_list.lower()}"><th colspan="6">{obj_list}</th></tr>\n'

        for row in rows:
            page += row

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/index.html", page)


# ---------------------------------------------------------------------------------------------------------------------
# Object Category and Tag Pages Generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_category_pages(db, objects_by_category):
    for category_id, category_name in db.categories.items():
        # Begin page
        page = PROLOGUE.format(f"Category: {category_name} | Super Mario Galaxy Object Database")
        page += f'\t\t\t<h1>Category: {category_name}</h1>\n'

        # Begin table
        page += '\t\t\t<table width="100%">\n' \
                '\t\t\t\t<tr>' \
                '<th colspan="2">Internal Name</th>' \
                '<th>Class Name</th>' \
                '<th>Description</th>' \
                '<th>Games</th>' \
                '<th>Archive</th>' \
                '</tr>\n'

        # Write table rows
        for row in objects_by_category[category_id]:
            page += row

        # Wrap up table and page
        page += "\t\t\t</table>\n"
        page += EPILOGUE
        write_strings_file(f"docs/category_{category_id}.html", page)


def generate_tag_pages(db, objects_by_progress):
    for tag_name, tag_rows in objects_by_progress.items():
        if tag_name == "Leftover":
            continue

        # Begin page
        page = PROLOGUE.format(f"{tag_name} objects | Super Mario Galaxy Object Database")
        page += f'\t\t\t<h1>{tag_name} objects</h1>\n'

        # Begin table
        page += '\t\t\t<table width="100%">\n' \
                '\t\t\t\t<tr>' \
                '<th colspan="2">Internal Name</th>' \
                '<th>Class Name</th>' \
                '<th>Description</th>' \
                '<th>Games</th>' \
                '<th>Archive</th>' \
                '</tr>\n'

        # Write table rows
        for row in tag_rows:
            page += row

        # Wrap up table and page
        page += "\t\t\t</table>\n"
        page += EPILOGUE
        write_strings_file(f"docs/tag_{tag_name}.html", page)


# ---------------------------------------------------------------------------------------------------------------------
# Classes Overview and Class Page Generation
# ---------------------------------------------------------------------------------------------------------------------
def generate_classes_overview_page(db):
    page = PROLOGUE.format("Classes Overview | Super Mario Galaxy Object Database")

    # Introduction
    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.\n' \
            '\t\t\t\tHere, you can find information about every object and class that can be used in the game.\n' \
            '\t\t\t\tThis page lists all classes in the <em>Galaxy</em> games. Go to the respective pages to learn\n' \
            '\t\t\t\tmore about an individual class.\n' \
            '\t\t\t</p>\n'

    # Progress table
    unknown_classes = len([c for c in db.classes.values() if c["Progress"] == 0])
    known_classes = len([c for c in db.classes.values() if c["Progress"] == 1])
    finished_classes = len([c for c in db.classes.values() if c["Progress"] == 2])
    total_classses = len(db.classes)
    unknown_classes_percent = round(unknown_classes / total_classses, 4) * 100
    known_classes_percent = round(known_classes / total_classses, 4) * 100
    finished_classes_percent = round(finished_classes / total_classses, 4) * 100

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
            f'<td>{total_classses}</td>' \
            f'</tr>\n' \
            '\t\t\t</table>\n'

    page += DOWNLOADS

    #  Begin table
    page += '\t\t\t<table width="100%">\n' \
            '\t\t\t\t<tr>' \
            '<th colspan="2">Class Name</th>' \
            '<th>Description</th>' \
            '<th>Games</th>' \
            '<th>Archive</th>' \
            '<th>File</th>' \
            '</tr>\n'

    for clazz in db.classes.values():
        class_href = f'<a href="class_{clazz["InternalName"]}.html">{clazz["InternalName"]}</a>'
        description = f'<details><summary>{clazz["InternalName"]}</summary><p>{clazz["Notes"]}</p></details>'
        list_name = clazz["List"]
        file_name = clazz["File"]
        games = GAMES[clazz["Games"]]

        progress_color = PROGRESS_TO_COLOR[clazz["Progress"]]

        row = '\t\t\t\t<tr>' \
              f'<td class="{progress_color}">&nbsp;</td>' \
              f'<td>{class_href}</td>' \
              f'<td>{description}</td>' \
              f'<td>{games}</td>' \
              f'<td>{file_name}</td>' \
              f'<td>{list_name}</td>' \
              '</tr>\n'

        page += row

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/classes.html", page)


ARGUMENTS = [
    "Obj_arg0", "Obj_arg1", "Obj_arg2", "Obj_arg3", "Obj_arg4", "Obj_arg5", "Obj_arg6", "Obj_arg7", "Path_arg0",
    "Path_arg1", "Path_arg2", "Path_arg3", "Path_arg4", "Path_arg5", "Path_arg6", "Path_arg7", "Point_arg0",
    "Point_arg1", "Point_arg2", "Point_arg3", "Point_arg4", "Point_arg5", "Point_arg6", "Point_arg7"
]
SWITCHES = [
    "SW_APPEAR", "SW_DEAD", "SW_A", "SW_B", "SW_PARAM", "SW_AWAKE"
]
PROPERTIES = [
    "Rail", "Group", "ClippingGroup", "DemoCast", "DemoSimpleCast", "Camera", "Message", "MapPartsRailMover",
    "MapPartsRailPosture", "MapPartsRailRotator", "MapPartsRotator", "MapPartsSeesaw1AxisRotator",
    "MapPartsSeesaw2AxisRotator", "MapPartsSeesaw2AxisRollerRotator", "MapPartsFloatingForce", "BaseMtxFollower",
    "BaseMtxFollowTarget"
]
DEFAULT_DESCS = {
    "SW_APPEAR": "If enabled, the object will appear.",
    "SW_PARAM": "If enabled, animations and update rates use ParamScale.",
    "SW_AWAKE": "If enabled, the object will become visible and resume movement.",
    "ClippingGroup": "Objects in this group are always clipped together.",
    "DemoSimpleCast": "TODO",
    "Message": "The text message ID to be used. Needs to be specified in the zone's text file.",
    "MapPartsRailMover": "TODO",
    "MapPartsRailPosture": "TODO",
    "MapPartsRailRotator": "TODO",
    "MapPartsRotator": "TODO",
    "MapPartsSeesaw1AxisRotator": "TODO",
    "MapPartsSeesaw2AxisRotator": "TODO",
    "MapPartsSeesaw2AxisRollerRotator": "TODO",
    "MapPartsFloatingForce": "TODO",
    "BaseMtxFollower": "Objects of this class can follow another BaseMtxFollowTarget object.",
    "BaseMtxFollowTarget": "Objects of this class can be followed by another BaseMtxFollower object."
}


def generate_class_pages(db):
    for actor in db.classes.values():
        # Begin page
        page = PROLOGUE.format(f'Class: {actor["InternalName"]} -- Super Mario Galaxy Object Database')
        page += f'\t\t\t<h1>Class: {actor["InternalName"]}</h1>\n'
        page += f'\t\t\t<p>{actor["Notes"]}</p>\n'

        # Determine what parameter categories to populate
        has_arguments = False
        for prop in ARGUMENTS:
            has_arguments |= prop in actor["Parameters"]
        has_switches = False
        for prop in SWITCHES:
            has_switches |= prop in actor["Parameters"]
        has_properties = False
        for prop in PROPERTIES:
            has_properties |= prop in actor["Parameters"]

        if has_arguments:
            page += f'\t\t\t<h2>Arguments</h2>\n'
            page += '\t\t\t<table width="100%">\n'
            page += '\t\t\t\t<tr><th>Name</th><th>Type</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th><th>Values</th></tr>\n'
            page += '\t\t\t\t<colgroup><col width=6%><col width=4%><col width=5%><col width=5%><col width=40%><col width=20%><col width=20%></colgroup>\n'

            for arg in ARGUMENTS:
                if arg not in actor["Parameters"]:
                    continue
                info = actor["Parameters"][arg]
                games = GAMES[info["Games"]]
                required = "yes" if info["Needed"] else "no"
                name = info["Name"]
                description = info["Description"] if arg not in DEFAULT_DESCS else DEFAULT_DESCS[arg]
                exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])
                values = "".join([f"<li>{value_info['Value']}: {value_info['Notes']}</li>" for value_info in info["Values"]])

                page += '\t\t\t\t<tr>' \
                        f'<td>{arg}</td>' \
                        f'<td>{info["Type"]}</td>' \
                        f'<td>{games}</td>' \
                        f'<td>{required}</td>' \
                        f'<td><p><b>{name}</b>: {description}</p></td>' \
                        f'<td><ul>{exclusives}</ul></td>' \
                        f'<td><ul>{values}</ul></td>' \
                        '</tr>\n'

            page += '\t\t\t</table>\n'

        if has_switches:
            page += f'\t\t\t<h2>Switches</h2>\n'
            page += '\t\t\t<table width="100%">\n'
            page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'
            page += '\t\t\t\t<colgroup><col width=10%><col width=5%><col width=5%><col width=50%><col width=30%></colgroup>\n'

            for switcharg in SWITCHES:
                if switcharg not in actor["Parameters"]:
                    continue
                info = actor["Parameters"][switcharg]
                games = GAMES[info["Games"]]
                required = "yes" if info["Needed"] else "no"
                description = info["Description"] if switcharg not in DEFAULT_DESCS else DEFAULT_DESCS[switcharg]
                exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])

                page += '\t\t\t\t<tr>' \
                        f'<td>{switcharg}</td>' \
                        f'<td>{games}</td>' \
                        f'<td>{required}</td>' \
                        f'<td><p>{description}</p></td>' \
                        f'<td><ul>{exclusives}</ul></td>' \
                        '</tr>\n'

            page += '\t\t\t</table>\n'

        if has_properties:
            page += f'\t\t\t<h2>Properties</h2>\n'
            page += '\t\t\t<table width="100%">\n'
            page += '\t\t\t\t<tr><th>Name</th><th>Games</th><th>Required?</th><th>Description</th><th>Exclusives?</th></tr>\n'

            for proparg in PROPERTIES:
                if proparg not in actor["Parameters"]:
                    continue
                info = actor["Parameters"][proparg]
                games = GAMES[info["Games"]]
                required = "yes" if info["Needed"] else "no"
                description = info["Description"] if proparg not in DEFAULT_DESCS else DEFAULT_DESCS[proparg]
                exclusives = "".join([f"<li>{l}</li>" for l in info["Exclusives"]])

                page += '\t\t\t\t<tr>' \
                        f'<td>{proparg}</td>' \
                        f'<td>{games}</td>' \
                        f'<td>{required}</td>' \
                        f'<td><p>{description}</p></td>' \
                        f'<td><ul>{exclusives}</ul></td>' \
                        '</tr>\n'

            page += '\t\t\t</table>\n'


        page += EPILOGUE
        write_strings_file(f'docs/class_{actor["InternalName"]}.html', page)


# ---------------------------------------------------------------------------------------------------------------------
# Generation Sequence and Entry Point
# ---------------------------------------------------------------------------------------------------------------------
def generate(db):
    # Prepare data holders
    objects_by_progress = {"Unknown": list(), "Known": list(), "Finished": list(), "Unused": list(), "Leftover": list()}
    objects_by_list = {l: list() for l in db.lists}
    objects_by_category = {c: list() for c in db.categories.keys()}

    pregenerate(db, objects_by_progress, objects_by_list, objects_by_category)
    generate_objects_overview_page(db, objects_by_progress, objects_by_list)
    generate_category_pages(db, objects_by_category)
    generate_tag_pages(db, objects_by_progress)

    generate_classes_overview_page(db)
    generate_class_pages(db)


if __name__ == '__main__':
    db = database.load_database()
    generate(db)
