import database
import os


def write_strings_file(file_path: str, strings):
    dirpath = os.path.dirname(file_path)
    os.makedirs(dirpath, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(strings)
        f.flush()


PROLOGUE = '<!DOCTYPE html>\n' \
           '<html>\n' \
           '	<head>\n' \
           '		<title>{0:s}</title>\n' \
           '		<link rel="shortcut icon" type="image/x-icon" href="../assets/icon.png">\n' \
           '		<link rel="stylesheet" href="normalize.css">\n' \
           '		<link rel="stylesheet" href="style.css">\n' \
           '		<meta name="keywords" content="Super,Mario,Galaxy,Object,Database,Documentation">\n' \
           '		<meta name="description" content="Super Mario Galaxy Object Database">\n' \
           '		<meta charset="UTF-8">\n' \
           '	</head>\n' \
           '	<body>\n' \
           '		<header>\n' \
           '			<h1><a href="index.html">Super Mario Galaxy Object Database</a></h1>\n' \
           '			<a href="objects.html">Objects</a> | \n' \
           '			<a href="classes.html">Classes</a>\n' \
           '		</header>\n' \
           '		<div class="contents">\n'
EPILOGUE = '		</div>\n' \
           '	</body>\n' \
           '</html>'
DOWNLOADS = '\t\t\t<p><a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.xml" download>' \
            'You can also download the latest database for Whitehole here.</a></p>\n'
PROGRESS_TO_COLOR = ["punknown", "pknown", "pfinished"]


def pregenerate(db, objects_by_progress, objects_by_list, objects_by_category, classes_by_progress):
    for obj in db.objects.values():
        class_href = f'<a href="class_{obj["ClassName"]}.html">{obj["ClassName"]}</a>'
        description = f'<details><summary>{obj["Name"]}</summary><p>{obj["Notes"]}</p></details>'
        list_name = db.classes[obj["ClassName"]]["List"]
        file_name = db.classes[obj["ClassName"]]["File"]

        # I want to customize this in the future...
        games = ""
        if obj["Games"] == 1:
            games = "SMG1"
        elif obj["Games"] == 2:
            games = "SMG2"
        elif obj["Games"] == 3:
            games = "Both"

        progress_color = PROGRESS_TO_COLOR[obj["Progress"]]

        row = '\t\t\t\t<tr>' \
              f'<td class="{progress_color}">&nbsp;</td>' \
              f'<td>{obj["InternalName"]}</td>' \
              f'<td>{class_href}</td>' \
              f'<td>{description}</td>' \
              f'<td>{games}</td>' \
              f'<td>{file_name}</td>' \
              '</tr>\n'

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

    for actor in db.classes.values():
        pass


def generate_index(db):
    page = PROLOGUE.format("Overview | Super Mario Galaxy Object Database")

    page += '\t\t\t<p>\n' \
            '\t\t\t\tWelcome to the object database for <b>Super Mario Galaxy</b> and <b>Super Mario Galaxy 2</b>.\n' \
            '\t\t\t\tHere, you can find information about every object and class that can be used in the game.\n' \
            '\t\t\t\tEvery object has a brief description whereas the detailed information about their functions,\n' \
            '\t\t\t\tproperties and setups can be found on the respective class pages. An auto-generated XML file\n' \
            '\t\t\t\tfor Whitehole can be downloaded as well.\n' \
            '\t\t\t</p>\n' \
            '\t\t\t<ul>\n' \
            '\t\t\t\t<li><a href="objects.html">Objects Overview</a></li>\n' \
            '\t\t\t\t<li><a href="classes.html">Classes Overview</a></li>\n' \
            '\t\t\t\t<li><a href="https://raw.githubusercontent.com/SunakazeKun/galaxydatabase/main/objectdb.xml" download>' \
            'Whitehole Database</a></li>\n' \
            '\t\t\t</ul>\n' \

    page += EPILOGUE

    write_strings_file("docs/index.html", page)


def generate_objects_overview_page(db, objects_by_progress, objects_by_list):
    page = PROLOGUE.format("Objects Overview | Super Mario Galaxy Object Database")

    # Table of contents
    page += '\t\t\t<div class="tableofcontents">\n' \
            '\t\t\t\t<table>\n' \
            '\t\t\t\t\t<tr><th>Contents</th><th>Categories</th></tr>\n' \
            '\t\t\t\t\t<tr>\n' \
            '\t\t\t\t\t\t<td><ol>\n'

    # Contents
    for obj_list in db.lists:
        # We don't need GeneralPosInfo lol
        if obj_list == "GeneralPosInfo":
            continue
        page += f'\t\t\t\t\t\t\t<li><a href="#{obj_list.lower()}">{obj_list}</a></li>\n'
    page += '\t\t\t\t\t\t</ol></td>\n' \
            '\t\t\t\t\t\t<td><ol>\n'
    # Categories
    for category_id, category_name in db.categories.items():
        page += f'\t\t\t\t\t\t\t<li><a href="category_{category_id}.html">{category_name}</a></li>\n'
    page += '\t\t\t\t\t\t</ol></td>\n' \
            '\t\t\t\t\t</tr>\n' \
            '\t\t\t\t</table>\n' \
            '\t\t\t</div>\n'

    # Introduction
    page += '\t\t\t<p>\n' \
            '\t\t\t\tLorem ipsum dolor bruh\n' \
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
            '<th><a href="tag_unknown.html">Unknown objects</a></th>' \
            '<th><a href="tag_known.html">Known objects</a></th>' \
            '<th><a href="tag_finished.html">Finished objects</a></th>' \
            '<th><a href="tag_unused.html">Unused objects</a></th>' \
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

    for obj_list, rows in objects_by_list.items():
        page += f'\t\t\t\t<tr id="{obj_list.lower()}"><th colspan="6">{obj_list}</th></tr>\n'

        for row in rows:
            page += row

    # Wrap up page
    page += "\t\t\t</table>\n"
    page += EPILOGUE
    write_strings_file("docs/objects.html", page)


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


def generate(db):
    objects_by_progress = {"Unknown": list(), "Known": list(), "Finished": list(), "Unused": list(), "Leftover": list()}
    objects_by_list = {l: list() for l in db.lists}
    objects_by_category = {c: list() for c in db.categories.keys()}
    classes_by_progress = {"Unknown": list(), "Known": list(), "Finished": list()}

    pregenerate(db, objects_by_progress, objects_by_list, objects_by_category, classes_by_progress)
    generate_index(db)
    generate_objects_overview_page(db, objects_by_progress, objects_by_list)
    generate_category_pages(db, objects_by_category)
    generate_tag_pages(db, objects_by_progress)


if __name__ == '__main__':
    db = database.load_database()
    generate(db)
