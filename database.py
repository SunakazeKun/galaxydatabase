import os
import json
import datetime
import math


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
    "DemoSimpleCast": (False, False, False, False),
    "MarioFaceShipNpcRegister": (False, False, False, False),
    "Camera": (False, False, True, False),
    "Message": (False, False, False, False),
    "AppearPowerStar": (False, False, True, False),
    "MapPartsRailMover": (False, False, False, False),
    "MapPartsRailPosture": (False, False, False, False),
    "MapPartsRailRotator": (False, False, False, False),
    "MapPartsRotator": (False, False, False, False),
    "MapPartsSeesaw1AxisRotator": (False, False, False, False),
    "MapPartsSeesaw2AxisRotator": (False, False, False, False),
    "MapPartsSeesaw2AxisRollerRotator": (False, False, False, False),
    "MapPartsFloatingForce": (False, False, False, False),
    "BaseMtxFollower": (False, False, False, False),
    "BaseMtxFollowTarget": (False, False, False, False),
}

__FIELD_COLUMN_ORDER__ = [
    "Game", "Zone", "Archive", "Layer", "File", "Obj_arg0", "Obj_arg1", "Obj_arg2", "Obj_arg3", "Obj_arg4", "Obj_arg5",
    "Obj_arg6", "Obj_arg7", "CommonPath_ID", "CameraSetId", "MessageId", "SW_APPEAR", "SW_DEAD", "SW_A", "SW_B",
    "SW_PARAM", "SW_AWAKE", "SW_SLEEP", "MoveConditionType", "RotateSpeed", "RotateAngle", "RotateAxis",
    "RotateAccelType", "RotateStopTime", "RotateType", "ShadowType", "SignMotionType", "PressType", "FarClip",
    "ParamScale", "ShapeModelNo", "AreaShapeNo", "Validity", "Range", "Distant", "Gravity_type", "Power", "Inverse",
    "Priority", "DemoName", "TimeSheetName", "DemoSkip", "GroupId", "ClippingGroupId", "ViewGroupId", "DemoGroupId",
    "CastId", "ParentID", "GeneratorID", "Obj_ID", "MapParts_ID", "FollowId"
]

FIELD_COLUMN_ORDER = __FIELD_COLUMN_ORDER__.index


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
            "DemoObjInfo", "ChildObjInfo", "SoundInfo", "StartInfo"
        ]
        self.area_shapes = ["Any", "BaseOriginCube", "CenterOriginCube", "Sphere", "Cylinder", "Bowl"]
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

    def _fix_actor_(self, key, actor):
        if "InternalName" not in actor or type(actor["InternalName"]) != str or actor["InternalName"] == "":
            return

        data = {
            "InternalName": actor["InternalName"],
            "Notes": actor.get("Notes", ""),
            "Games": actor.get("Games", 0),
            "Progress": actor.get("Progress", 0),
            "Parameters": actor.get("Parameters", dict())
        }
        self._fix_properties_(data)

        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.classes[key] = data

    def _fix_object_(self, key, obj):
        if "InternalName" not in obj or type(obj["InternalName"]) != str or obj["InternalName"] == "":
            return

        data = {
            "InternalName": obj["InternalName"],
            "ClassNameSMG1": obj.get("ClassNameSMG1", ""),
            "ClassNameSMG2": obj.get("ClassNameSMG2", ""),
            "Name": obj.get("Name", ""),
            "Notes": obj.get("Notes", ""),
            "Category": obj.get("Category", "unknown"),
            "AreaShape": obj.get("AreaShape", "Any"),
            "ListSMG1": obj.get("ListSMG1", "ObjInfo"),
            "ListSMG2": obj.get("ListSMG2", "ObjInfo"),
            "File": obj.get("File", "Map"),
            "Games": obj.get("Games", 0),
            "Progress": obj.get("Progress", 0),
            "IsUnused": obj.get("IsUnused", False),
            "IsLeftover": obj.get("IsLeftover", False),
        }

        #if data["ClassNameSMG1"] not in self.classes:
        #    raise KeyError(f"Missing class: {data['ClassNameSMG1']}")
        #if data["ClassNameSMG2"] not in self.classes:
        #    raise KeyError(f"Missing class: {data['ClassNameSMG2']}")
        if data["Category"] not in self.categories:
            data["Category"] = "deprecated"
        if data["AreaShape"] not in self.area_shapes:
            data["AreaShape"] = "Any"
        if data["ListSMG1"] not in self.lists:
            data["ListSMG1"] = "ObjInfo"
        if data["ListSMG2"] not in self.lists:
            data["ListSMG2"] = "ObjInfo"
        if data["File"] not in self.archives:
            data["File"] = "Map"
        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.objects[key] = data

    def save_all(self):
        # Write source files
        for name, data in self.classes.items():
            path = os.path.join("data", "classes", name + ".json")
            write_json(path, data)

        for name, data in self.objects.items():
            path = os.path.join("data", "objects", name + ".json")
            write_json(path, data)

        write_json("data/categories.json", self.categories)

        # Write assembled JSON database
        alldata = {
            "Timestamp": math.floor(datetime.datetime.now().timestamp()),
            "Classes": self.classes,
            "Objects": self.objects,
            "Categories": list({"Key": k, "Description": d} for (k, d) in self.categories.items())
        }
        write_json("objectdb.json", alldata)


# ----------------------------------------------------------------------------------------------------------------------
# Initialization using the data in the objects and classes folders, categories.json and occurrences.json
# ----------------------------------------------------------------------------------------------------------------------
def load_database() -> GalaxyDatabase:
    db = GalaxyDatabase()

    # Occurrences
    db.occurrences = read_json("data/occurrences.json")

    # Categories
    try:
        for key, desc in read_json("data/categories.json").items():
            db.categories[key] = desc
    except:
        db.categories["unknown"] = "Uncategorized"

    # Classes
    for file in filter(lambda f: f.endswith(".json"), os.listdir("data/classes")):
        actor = read_json(os.path.join("data", "classes", file))
        db._fix_actor_(file.replace(".json", ""), actor)

    # Objects
    for file in filter(lambda f: f.endswith(".json"), os.listdir("data/objects")):
        obj = read_json(os.path.join("data", "objects", file))
        db._fix_object_(file.replace(".json", ""), obj)

    return db
