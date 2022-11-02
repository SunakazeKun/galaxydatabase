import os
import json
import sys
import traceback

from datetime import datetime
from math import floor


def _read_json_(file_path):
    if not os.path.exists(file_path):
        print(f"FATAL! The file {file_path} does not exist!")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print(f"FATAL! Failed to parse {file_path}")
        print(traceback.format_exc())
        sys.exit(1)


def _write_json_(file_path, data, indent: bool = True):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4 if indent else None, ensure_ascii=False)
    except Exception:
        print(f"An error occurred while trying to write {file_path}")
        print(traceback.format_exc())


# ----------------------------------------------------------------------------------------------------------------------
# Object and class properties
# ----------------------------------------------------------------------------------------------------------------------
OBJECT_LISTS = [
    "ObjInfo", "MapPartsInfo", "AreaObjInfo", "CameraCubeInfo", "PlanetObjInfo", "DemoObjInfo", "ChildObjInfo",
    "SoundInfo", "StartInfo"
]
OBJECT_ARCHIVES = ["Map", "Sound", "Design"]
PROPERTY_TYPES = ["Integer", "Float", "Boolean"]
AREA_SHAPES = ["Any", "BaseOriginCube", "CenterOriginCube", "Sphere", "Cylinder", "Bowl"]

__PROPERTY_FIELD_INFO__ = {
    # Enables: Name, Type, Description, Values, Needable

    # Arguments
    "Obj_arg0": (True, True, True, True, True),
    "Obj_arg1": (True, True, True, True, True),
    "Obj_arg2": (True, True, True, True, True),
    "Obj_arg3": (True, True, True, True, True),
    "Obj_arg4": (True, True, True, True, True),
    "Obj_arg5": (True, True, True, True, True),
    "Obj_arg6": (True, True, True, True, True),
    "Obj_arg7": (True, True, True, True, True),
    "Path_arg0": (True, True, True, True, True),
    "Path_arg1": (True, True, True, True, True),
    "Path_arg2": (True, True, True, True, True),
    "Path_arg3": (True, True, True, True, True),
    "Path_arg4": (True, True, True, True, True),
    "Path_arg5": (True, True, True, True, True),
    "Path_arg6": (True, True, True, True, True),
    "Path_arg7": (True, True, True, True, True),
    "Point_arg0": (True, True, True, True, True),
    "Point_arg1": (True, True, True, True, True),
    "Point_arg2": (True, True, True, True, True),
    "Point_arg3": (True, True, True, True, True),
    "Point_arg4": (True, True, True, True, True),
    "Point_arg5": (True, True, True, True, True),
    "Point_arg6": (True, True, True, True, True),
    "Point_arg7": (True, True, True, True, True),
    "RailObj_arg0": (True, True, True, True, True),
    "RailObj_arg1": (True, True, True, True, True),
    "RailObj_arg2": (True, True, True, True, True),
    "RailObj_arg3": (True, True, True, True, True),
    "RailObj_arg4": (True, True, True, True, True),
    "RailObj_arg5": (True, True, True, True, True),
    "RailObj_arg6": (True, True, True, True, True),
    "RailObj_arg7": (True, True, True, True, True),
    "MoveConditionType": (True, True, True, True, True),
    "RotateSpeed": (True, True, True, True, True),
    "RotateAngle": (True, True, True, True, True),
    "RotateAxis": (True, True, True, True, True),
    "RotateAccelType": (True, True, True, True, True),
    "RotateStopTime": (True, True, True, True, True),
    "RotateType": (True, True, True, True, True),
    "ShadowType": (True, True, True, True, True),
    "SignMotionType": (True, True, True, True, True),
    "PressType": (True, True, True, True, True),

    # Switches (name, type & values should be disabled)
    "SW_APPEAR": (False, False, True, False, True),
    "SW_DEAD": (False, False, True, False, True),
    "SW_A": (False, False, True, False, True),
    "SW_B": (False, False, True, False, True),
    "SW_PARAM": (False, False, True, False, False),
    "SW_AWAKE": (False, False, True, False, False),

    # Setup (name, type & values should be disabled)
    "Rail": (False, False, True, False, True),
    "Group": (False, False, True, False, True),
    "ClippingGroup": (False, False, True, False, False),
    "MercatorTransform": (False, False, True, False, True),
    "GeneralPos": (False, False, True, False, True),
    "Message": (False, False, True, False, True),
    "Camera": (False, False, True, False, True),
    "DemoCast": (False, False, True, False, True),
    "MarioFaceShipNpcRegister": (False, False, True, False, True),
    "AppearPowerStar": (False, False, True, False, True),
    "BaseMtxFollower": (False, False, True, False, False),
    "BaseMtxFollowTarget": (False, False, True, False, False),

    # Properties (name, type, values & needable should be disabled)
    "ScoreAttack": (False, False, True, False, False),
    "YoshiLockOnTarget": (False, False, True, False, False),
    "SearchTurtle": (False, False, True, False, False),
    "MirrorActor": (False, False, True, False, False),
    "DemoSimpleCast": (False, False, True, False, False),
    "MoveLimitCollision": (False, False, True, False, False),
    "MapPartsSeesaw1AxisRotator": (False, False, False, False, False),
    "MapPartsSeesaw2AxisRotator": (False, False, False, False, False),
    "MapPartsSeesaw2AxisRollerRotator": (False, False, False, False, False),
    "MapPartsFloatingForce": (False, False, False, False, False),
    "FloaterFloatingForceTypeNormal": (False, False, False, False, False),
}

__FIELD_DEFAULT_DESCRIPTIONS__ = {
    "SW_APPEAR": "The object will appear when this switch is activated.",
    "SW_DEAD": "Gets activated when it dies.",
    "SW_PARAM": "Animations, velocity and update rates are adjusted with ParamScale while this switch is activated.",
    "SW_AWAKE": "The object will become visible and resume movement when this switch is activated.",
    "ClippingGroup": "Objects in this group are always clipped together.",
    "MercatorTransform": "The object can use mercator projection for placement.",
    "Message": "The text message ID to be used. Needs to be specified in the zone's text file.",
    "MarioFaceShipNpcRegister": "This object can be registered to a Starship Mario NPC appearance event.",
    "BaseMtxFollower": "Objects of this class can follow another BaseMtxFollowTarget object.",
    "BaseMtxFollowTarget": "Objects of this class can be followed by another BaseMtxFollower object.",
    "YoshiLockOnTarget": "This object can be targeted by Yoshi.",
    "SearchTurtle": "Red Koopa Shells and Gold Shells home in on this object.",
    "MirrorActor": "A mirrored version of this object is created for mirror reflection setups if placed inside a MirrorArea.",
    "DemoSimpleCast": "This object will not pause its movement during cutscenes, NPC conversations, etc.",
    "MoveLimitCollision": "The object's collision binder also checks for MoveLimit collision."
}

__FIELD_DEFAULT_VALUES__ = {
    "DemoName": "",
    "Distant": 0.0,
    "Gravity_type": "Normal",
    "ParamScale": 1.0,
    "Power": "Normal",
    "Range": 0.0,
    "TimeSheetName": "",
    "Validity": ""
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


def all_properties():
    return list(__PROPERTY_FIELD_INFO__.keys())


def property_info(key: str):
    if key in __PROPERTY_FIELD_INFO__:
        return __PROPERTY_FIELD_INFO__[key]
    return False, False, False, False, False


def default_field_description(key: str):
    return __FIELD_DEFAULT_DESCRIPTIONS__[key] if key in __FIELD_DEFAULT_DESCRIPTIONS__ else ""


def default_field_value(key: str):
    return __FIELD_DEFAULT_VALUES__[key] if key in __FIELD_DEFAULT_VALUES__ else -1


# ----------------------------------------------------------------------------------------------------------------------
# Database holder definition
# ----------------------------------------------------------------------------------------------------------------------
class GalaxyDatabase:
    def __init__(self):
        self.objects = dict()
        self.classes = dict()
        self.categories = dict()
        self.occurrences = dict()

    def _load_(self):
        self.occurrences = _read_json_("data/occurrences.json")
        self.categories = _read_json_("data/categories.json")

        for file in filter(lambda f: f.endswith(".json"), os.listdir("data/classes")):
            clazz = _read_json_(os.path.join("data/classes", file))
            self._register_class_(clazz)

        for file in filter(lambda f: f.endswith(".json"), os.listdir("data/objects")):
            obj = _read_json_(os.path.join("data/objects", file))
            self._register_object_(obj)

    def _register_object_(self, raw):
        if "InternalName" not in raw or type(raw["InternalName"]) != str or raw["InternalName"] == "":
            return

        key = raw["InternalName"]

        # Copy ensures that the structure and order is correct
        data = {
            "InternalName": key,
            "ClassNameSMG1": raw.get("ClassNameSMG1", ""),
            "ClassNameSMG2": raw.get("ClassNameSMG2", ""),
            "Name": raw.get("Name", key),
            "Notes": raw.get("Notes", ""),
            "Category": raw.get("Category", "deprecated"),
            "AreaShape": raw.get("AreaShape", "Any"),
            "ListSMG1": raw.get("ListSMG1", "ObjInfo"),
            "ListSMG2": raw.get("ListSMG2", "ObjInfo"),
            "File": raw.get("File", "Map"),
            "Games": raw.get("Games", 0),
            "Progress": raw.get("Progress", 0),
            "IsUnused": raw.get("IsUnused", False),
            "IsLeftover": raw.get("IsLeftover", False)
        }

        # Ensure correct values for fields
        if data["Category"] not in self.categories:
            data["Category"] = "deprecated"
        if data["AreaShape"] not in AREA_SHAPES:
            data["AreaShape"] = "Any"
        if data["ListSMG1"] not in OBJECT_LISTS:
            data["ListSMG1"] = "ObjInfo"
        if data["ListSMG2"] not in OBJECT_LISTS:
            data["ListSMG2"] = "ObjInfo"
        if data["File"] not in OBJECT_ARCHIVES:
            data["File"] = "Map"
        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.objects[key] = data

    def _register_class_(self, raw):
        if "InternalName" not in raw or type(raw["InternalName"]) != str or raw["InternalName"] == "":
            return

        key = raw["InternalName"]

        # Copy ensures that the structure and order is correct
        data = {
            "InternalName": key,
            "Notes": raw.get("Notes", ""),
            "Games": raw.get("Games", 0),
            "Progress": raw.get("Progress", 0),
            "Parameters": raw.get("Parameters", dict())
        }
        self._register_properties_(data)

        # Ensure correct values for fields
        if data["Progress"] < 0:
            data["Progress"] = 0
        elif data["Progress"] > 2:
            data["Progress"] = 2

        self.classes[key] = data

    def _register_properties_(self, actor):
        properties = dict()

        for key in __PROPERTY_FIELD_INFO__.keys():
            if key not in actor["Parameters"]:
                continue

            enable_name, enable_type, enable_desc, enable_values, enable_needed = __PROPERTY_FIELD_INFO__[key]
            data = actor["Parameters"][key]

            # Copy ensures that the structure and order is correct
            prop = dict()

            if enable_name:
                prop["Name"] = data.get("Name", "")
            if enable_type:
                prop["Type"] = data.get("Type", "Integer")
            prop["Games"] = data.get("Games", 0)
            if enable_needed:
                prop["Needed"] = data.get("Needed", False)
            if enable_desc:
                prop["Description"] = data.get("Description", default_field_description(key))
            if enable_values:
                prop["Values"] = data.get("Values", list())
            prop["Exclusives"] = data.get("Exclusives", list())

            properties[key] = prop

        actor["Parameters"] = properties

    def save_all(self):
        # Write raw database files
        print("Writing categories.json ...")
        _write_json_("data/categories.json", self.categories)

        print("Writing classes ...")
        for name, data in self.classes.items():
            path = os.path.join("data", "classes", name + ".json")
            _write_json_(path, data)

        print("Writing objects ...")
        for name, data in self.objects.items():
            path = os.path.join("data", "objects", name + ".json")
            _write_json_(path, data)

        # Write assembled JSON database
        print("Writing objectdb.json ...")
        assembled_db = {
            "Timestamp": floor(datetime.now().timestamp()),
            "Classes": list(self.classes.values()),
            "Objects": list(self.objects.values()),
            "Categories": list({"Key": k, "Description": d} for (k, d) in self.categories.items())
        }
        _write_json_("objectdb.json", assembled_db, False)


def load_database() -> GalaxyDatabase:
    db = GalaxyDatabase()
    db._load_()
    return db
