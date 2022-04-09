import os
import json


def read_json(file_path):
    print(f"Reading {file_path} ...")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(file_path, data):
    print(f"Writing {file_path} ...")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()


__FIELD_DEFAULTS__ = {
    "AreaShapeNo": -1,
    "CameraSetId": -1,
    "CastId": -1,
    "ClippingGroupId": -1,
    "CommonPath_ID": -1,
    "DemoGroupId": -1,
    "DemoName": "",
    "DemoSkip": -1,
    "Distant": 0.0,
    "FarClip": -1,
    "FollowId": -1,
    "GeneratorID": -1,
    "Gravity_type": "Normal",
    "GroupId": -1,
    "Inverse": -1,
    "MapParts_ID": -1,
    "MessageId": -1,
    "MoveConditionType": -1,
    "Obj_ID": -1,
    "Obj_arg0": -1,
    "Obj_arg1": -1,
    "Obj_arg2": -1,
    "Obj_arg3": -1,
    "Obj_arg4": -1,
    "Obj_arg5": -1,
    "Obj_arg6": -1,
    "Obj_arg7": -1,
    "ParamScale": 1.0,
    "ParentID": -1,
    "Power": "Normal",
    "PressType": -1,
    "Priority": -1,
    "Range": 0.0,
    "RotateAccelType": -1,
    "RotateAngle": -1,
    "RotateAxis": -1,
    "RotateSpeed": -1,
    "RotateStopTime": -1,
    "RotateType": -1,
    "SW_A": -1,
    "SW_APPEAR": -1,
    "SW_AWAKE": -1,
    "SW_B": -1,
    "SW_DEAD": -1,
    "SW_PARAM": -1,
    "SW_SLEEP": -1,
    "ShadowType": -1,
    "ShapeModelNo": -1,
    "SignMotionType": -1,
    "TimeSheetName": "",
    "Validity": "",
    "ViewGroupId": -1
}
__FIELD_EDITOR_INFO__ = {
    # Enables: Name, Type, Description, Values
    "Obj_arg0": (True, True, True, True),
    "Obj_arg1": (True, True, True, True),
    "Obj_arg2": (True, True, True, True),
    "Obj_arg3": (True, True, True, True),
    "Obj_arg4": (True, True, True, True),
    "Obj_arg5": (True, True, True, True),
    "Obj_arg6": (True, True, True, True),
    "Obj_arg7": (True, True, True, True),
    "Path_arg0": (True, True, True, True),
    "Path_arg1": (True, True, True, True),
    "Path_arg2": (True, True, True, True),
    "Path_arg3": (True, True, True, True),
    "Path_arg4": (True, True, True, True),
    "Path_arg5": (True, True, True, True),
    "Path_arg6": (True, True, True, True),
    "Path_arg7": (True, True, True, True),
    "Point_arg0": (True, True, True, True),
    "Point_arg1": (True, True, True, True),
    "Point_arg2": (True, True, True, True),
    "Point_arg3": (True, True, True, True),
    "Point_arg4": (True, True, True, True),
    "Point_arg5": (True, True, True, True),
    "Point_arg6": (True, True, True, True),
    "Point_arg7": (True, True, True, True),
    "SW_APPEAR": (False, False, False, False),
    "SW_DEAD": (False, False, True, False),
    "SW_A": (False, False, True, False),
    "SW_B": (False, False, True, False),
    "SW_PARAM": (False, False, False, False),
    "SW_AWAKE": (False, False, False, False),
    "Rail": (False, False, True, False),
    "Group": (False, False, True, False),
    "ClippingGroup": (False, False, False, False),
    "DemoCast": (False, False, True, False),
    "Camera": (False, False, True, False),
    "Message": (False, False, False, False),
    "ShadowType": (False, False, True, True),
    "MoveConditionType": (False, False, True, True),
    "RotateSpeed": (False, False, True, False),
    "RotateAngle": (False, False, True, False),
    "RotateAxis": (False, False, True, True),
    "RotateAccelType": (False, False, True, True),
    "RotateStopTime": (False, False, True, False),
    "RotateType": (False, False, True, True),
    "SignMotionType": (False, False, True, True),
    "BaseMtxFollower": (False, False, False, False),
    "BaseMtxFollowTarget": (False, False, False, False),
}


def default_field_value(key: str):
    if key in __FIELD_DEFAULTS__:
        return __FIELD_DEFAULTS__[key]
    return "n/a"


def field_info(key: str):
    if key in __FIELD_EDITOR_INFO__:
        return __FIELD_EDITOR_INFO__[key]
    return False, False, False, False


def all_fields():
    return list(__FIELD_EDITOR_INFO__.keys())


# ----------------------------------------------------------------------------------------------------------------------
# Database holder definition
# ----------------------------------------------------------------------------------------------------------------------
class GalaxyDatabase:
    def __init__(self):
        self.objects = dict()
        self.classes = dict()
        self.categories = dict()
        self.occurrences = dict()

        self.lists = [
            "ObjInfo", "MapPartsInfo", "AreaObjInfo", "CameraCubeInfo", "PlanetObjInfo",
            "DemoObjInfo", "ChildObjInfo", "SoundInfo", "StartInfo", "GeneralPosInfo"
        ]
        self.archives = ["Map", "Sound", "Design"]
        self.field_types = ["Integer", "Float", "Boolean"]

    def _fix_properties_(self, actor):
        newprops = dict()

        for key in __FIELD_EDITOR_INFO__.keys():
            if key not in actor["Parameters"]:
                continue

            enable_name, enable_type, enable_desc, enable_values = __FIELD_EDITOR_INFO__[key]
            data = actor["Parameters"][key]
            prop = dict()

            if enable_name:
                prop["Name"] = data.get("Name", "")
            if enable_type:
                prop["Type"] = data.get("Type", "Integer")
            prop["Games"] = data.get("Games", 0)
            prop["Needed"] = data.get("Needed", False)
            if enable_desc:
                prop["Description"] = data.get("Description", "")
            if enable_values:
                prop["Values"] = data.get("Values", list())
            prop["Exclusives"] = data.get("Exclusives", list())

            newprops[key] = prop

        actor["Parameters"] = newprops

    def _fix_actor_(self, actor):
        if "InternalName" not in actor or type(actor["InternalName"]) != str or actor["InternalName"] == "":
            return

        data = {
            "InternalName": actor["InternalName"],
            "Notes": actor.get("Notes", ""),
            "Games": actor.get("Games", 0),
            "Progress": actor.get("Progress", 0),
            "List": actor.get("List", "ObjInfo"),
            "File": actor.get("File", "Map"),
            "Parameters": actor.get("Parameters", dict())
        }
        self._fix_properties_(data)

        if data["List"] not in self.lists:
            data["List"] = "ObjInfo"
            print(f"Overriding List for actor {actor['InternalName']}")
        if data["File"] not in self.archives:
            data["File"] = "Map"
            print(f"Overriding File for actor {actor['InternalName']}")

        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.classes[data["InternalName"]] = data

    def _fix_object_(self, obj):
        if "InternalName" not in obj or type(obj["InternalName"]) != str or obj["InternalName"] == "":
            return

        data = {
            "InternalName": obj["InternalName"],
            "ClassName": obj.get("ClassName", ""),
            "Name": obj.get("Name", ""),
            "Notes": obj.get("Notes", ""),
            "Category": obj.get("Category", "unknown"),
            "Games": obj.get("Games", 0),
            "Progress": obj.get("Progress", 0),
            "IsUnused": obj.get("IsUnused", False),
            "IsLeftover": obj.get("IsLeftover", False),
        }

        if data["ClassName"] not in self.classes:
            raise KeyError(f"Missing class: {data['ClassName']}")
        if data["Category"] not in self.categories:
            data["Category"] = "unknown"
        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.objects[data["InternalName"]] = data

    def save_all(self):
        # def create_or_clear(folder):
        #     if os.path.exists(folder):
        #         for file in filter(lambda f: f.endswith(".json"), os.listdir(folder)):
        #             os.unlink(os.path.join(folder, file))
        #     else:
        #         os.mkdir(folder)
        # create_or_clear("data/classes")
        # create_or_clear("data/objects")

        for name, data in self.classes.items():
            path = os.path.join("data", "classes", name + ".json")
            write_json(path, data)

        for name, data in self.objects.items():
            path = os.path.join("data", "objects", name + ".json")
            write_json(path, data)

        write_json("data/categories.json", self.categories)


# ----------------------------------------------------------------------------------------------------------------------
# Initialization using the data in the objects and classes folders as well as categories.json
# ----------------------------------------------------------------------------------------------------------------------
def load_database() -> GalaxyDatabase:
    db = GalaxyDatabase()

    # Occurrences
    db.occurrences = read_json("data/occurrences.json")

    # Categories
    try:
        for key, desc in read_json("data/categories.json").items():
            db.categories[key] = desc

        if "unknown" not in db.categories:
            db.categories["unknown"] = "Unknown"
    except:
        db.categories["unknown"] = "Unknown"

    # Classes
    for file in filter(lambda f: f.endswith(".json"), os.listdir("data/classes")):
        actor = read_json(os.path.join("data", "classes", file))
        db._fix_actor_(actor)

    # Objects
    for file in filter(lambda f: f.endswith(".json"), os.listdir("data/objects")):
        obj = read_json(os.path.join("data", "objects", file))
        db._fix_object_(obj)

    return db
