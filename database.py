from __future__ import annotations
from datetime import datetime
from math import floor
from typing import Any
import os
import json


def load_database():
    galaxy_db = GalaxyDatabase()
    galaxy_db.initialize()
    return galaxy_db


class GalaxyDatabase:
    def __init__(self):
        self.objects: dict[str, GalaxyObject] = {}
        self.configs: dict[str, GalaxyConfig] = {}
        self.categories: dict[str, str] = {}
        self.occurrences: dict[str, list] = {}

    def initialize(self):
        self.categories = _read_json_("data/categories.json")
        self.occurrences = _read_json_("data/occurrences.json")

        # Load configs
        for file in filter(lambda f: f.endswith(".json"), os.listdir("data/configs")):
            raw_config = _read_json_(os.path.join("data/configs", file))
            galaxy_config = GalaxyConfig(raw_config)
            self.configs[galaxy_config.internal_name] = galaxy_config

        # Load objects
        raw_objects = _read_json_("data/objects.json")

        for raw_object in sorted(raw_objects, key=lambda o: o["InternalName"].lower()):
            galaxy_object = GalaxyObject(raw_object)
            self.objects[galaxy_object.internal_name] = galaxy_object

    def save_all(self):
        print("Writing categories.json")
        _write_json_("data/categories.json", self.categories)
        # _write_json_("data/occurrences.json", self.occurrences)

        # Write configs
        print("Writing configs...")
        raw_configs = []
        for galaxy_config in self.configs.values():
            raw_config = galaxy_config.as_json()
            raw_configs.append(raw_config)

            _write_json_(f"data/configs/{galaxy_config.internal_name}.json", raw_config)
        raw_configs.sort(key=lambda c: c["InternalName"].lower())

        # Write objects
        print("Writing objects.json")
        raw_objects = [o.as_json() for o in self.objects.values()]
        raw_objects.sort(key=lambda o: o["InternalName"].lower())
        _write_json_("data/objects.json", raw_objects)

        # Write objectdb.json
        print("Writing objectdb.json")
        assembled_db = {
            "Timestamp": floor(datetime.now().timestamp()),
            "Classes": raw_configs,
            "Objects": raw_objects,
            "Categories": list({"Key": k, "Description": d} for (k, d) in self.categories.items())
        }
        _write_json_("objectdb.json", assembled_db, False)


class GalaxyObject:
    def __init__(self, data: dict[str, Any] = None, internal_name: str = None):
        if data is None:
            data = {}

            if internal_name is None:
                raise AttributeError("Cannot initialize object without data or internal name")

        self.internal_name: str = get_str(data, "InternalName", internal_name)
        self.config_name_smg1: str = get_str(data, "ClassNameSMG1")
        self.config_name_smg2: str = get_str(data, "ClassNameSMG2")
        self.name: str = get_str(data, "Name", internal_name)
        self.notes: str = get_str(data, "Notes")
        self.category: str = get_str(data, "Category", "unknown")

        self.area_shape: str = get_str(data, "AreaShape", "Any")

        self.list_smg1: str = get_str(data, "ListSMG1", "ObjInfo")
        self.list_smg2: str = get_str(data, "ListSMG2", "ObjInfo")
        self.file: str = get_str(data, "File", "Map")
        self.games: int = get_int(data, "Games")

        self.progress: int = get_int(data, "Progress")
        self.is_unused: bool = get_bool(data, "IsUnused")
        self.is_leftover: bool = get_bool(data, "IsLeftover")

    def as_json(self) -> dict[str, Any]:
        return {
            "InternalName": self.internal_name,
            "ClassNameSMG1": self.config_name_smg1,
            "ClassNameSMG2": self.config_name_smg2,
            "Name": self.name,
            "Notes": self.notes,
            "Category": self.category,
            "AreaShape": self.area_shape,
            "ListSMG1": self.list_smg1,
            "ListSMG2": self.list_smg2,
            "File": self.file,
            "Games": self.games,
            "Progress": self.progress,
            "IsUnused": self.is_unused,
            "IsLeftover": self.is_leftover
        }


class GalaxyConfig:
    def __init__(self, data: dict[str, Any] = None, internal_name: str = None):
        if data is None:
            data = {}

            if internal_name is None:
                raise AttributeError("Cannot initialize config without data or internal name")

        self.internal_name: str = get_str(data, "InternalName", internal_name)
        self.notes: str = get_str(data, "Notes")
        self.games: int = get_int(data, "Games")
        self.progress: int = get_int(data, "Progress")
        self.properties: dict[str, GalaxyConfigProperty] = {}

        raw_parameters = get_dict(data, "Parameters")

        for key, raw_parameter in raw_parameters.items():
            config_property = GalaxyConfigProperty(key, raw_parameter)
            self.properties[key] = config_property

    def as_json(self) -> dict[str, Any]:
        raw_parameters: list[GalaxyConfigProperty] = list(self.properties.values())
        raw_parameters.sort(key=lambda p: __CACHED_PROPERTY_KEYS__.index(p.identifier))

        return {
            "InternalName": self.internal_name,
            "Notes": self.notes,
            "Games": self.games,
            "Progress": self.progress,
            "Parameters": {p.identifier: p.as_json() for p in raw_parameters}
        }


class GalaxyConfigProperty:
    def __init__(self, property_name: str, data: dict[str, Any] = None):
        if property_name is None:
            raise AttributeError("Cannot initialize property without name")
        if data is None:
            data = {}

        property_info = get_property_info(property_name)
        self.identifier: str = property_name
        self.name = get_str(data, "Name", "<unnamed>") if property_info.use_name else ""
        self.type = get_str(data, "Type", "Integer") if property_info.use_type else "Integer"
        self.games = get_int(data, "Games")
        self.needed = get_bool(data, "Needed") if property_info.use_need else False
        self.description = get_str(data, "Description", property_info.default_description)
        self.values = get_list(data, "Values") if property_info.use_values else []
        self.exclusives = get_list(data, "Exclusives")

    def as_json(self) -> dict[str, Any]:
        property_info = get_property_info(self.identifier)
        result = {}

        if property_info.use_name:
            result["Name"] = self.name
        if property_info.use_type:
            result["Type"] = self.type
        result["Games"] = self.games
        if property_info.use_need:
            result["Needed"] = self.needed
        result["Description"] = self.description
        result["Values"] = self.values
        result["Exclusives"] = self.exclusives

        return result


# ----------------------------------------------------------------------------------------------------------------------
# Generic object & config attribute values

OBJECT_LISTS = ["ObjInfo", "MapPartsInfo", "AreaObjInfo", "CameraCubeInfo", "PlanetObjInfo", "DemoObjInfo",
                "ChildObjInfo", "SoundInfo", "StartInfo"]
OBJECT_ARCHIVES = ["Map", "Sound", "Design"]
PROPERTY_TYPES = ["Integer", "Float", "Boolean"]
AREA_SHAPES = ["Any", "BaseOriginCube", "CenterOriginCube", "Sphere", "Cylinder", "Bowl"]


# ----------------------------------------------------------------------------------------------------------------------
# Property helpers

__PROPERTY_INFOS__: dict[str, PropertyInfo] = {}
__CACHED_PROPERTY_KEYS__: list[str] = []


class PropertyInfo:
    def __init__(self, property_name: str, category_name: str, use_name: bool = False, use_type: bool = False,
                 use_values: bool = False, use_need: bool = False, default_description: str = ""):
        self.property_name: str = property_name
        self.category_name: str = category_name
        self.use_name = use_name
        self.use_type = use_type
        self.use_values = use_values
        self.use_need = use_need
        self.default_description = default_description

        if property_name is not None and property_name != "":
            __PROPERTY_INFOS__[property_name] = self
            __CACHED_PROPERTY_KEYS__.append(property_name)


def get_property_info(property_name: str) -> PropertyInfo:
    if property_name in __PROPERTY_INFOS__:
        return __PROPERTY_INFOS__[property_name]
    return __DEFAULT_PROPERTY_INFO__


__DEFAULT_PROPERTY_INFO__ = PropertyInfo("", "dummy")


# General arguments
PropertyInfo("Obj_arg0", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg1", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg2", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg3", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg4", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg5", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg6", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Obj_arg7", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg0", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg1", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg2", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg3", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg4", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg5", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg6", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Path_arg7", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg0", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg1", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg2", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg3", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg4", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg5", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg6", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("Point_arg7", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg0", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg1", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg2", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg3", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg4", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg5", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg6", "arg", use_name=True, use_type=True, use_values=True, use_need=True)
PropertyInfo("RailObj_arg7", "arg", use_name=True, use_type=True, use_values=True, use_need=True)

# MapParts arguments
PropertyInfo("MoveConditionType", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("RotateSpeed", "mapparts_arg", use_name=True)
PropertyInfo("RotateAngle", "mapparts_arg", use_name=True)
PropertyInfo("RotateAxis", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("RotateAccelType", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("RotateStopTime", "mapparts_arg", use_name=True)
PropertyInfo("RotateType", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("ShadowType", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("SignMotionType", "mapparts_arg", use_name=True, use_values=True)
PropertyInfo("PressType", "mapparts_arg", use_name=True, use_values=True)

# Switches
PropertyInfo("SW_APPEAR", "switch", use_need=True, default_description="The object will appear when this switch is activated.")
PropertyInfo("SW_DEAD", "switch", use_need=True, default_description="Gets activated when it dies.")
PropertyInfo("SW_A", "switch", use_need=True)
PropertyInfo("SW_B", "switch", use_need=True)
PropertyInfo("SW_PARAM", "switch", use_need=False, default_description="Animations, velocity and update rates are adjusted with ParamScale while this switch is activated.")
PropertyInfo("SW_AWAKE", "switch", use_need=False, default_description="The object will become visible and resume movement when this switch is activated.")

# Other setup
PropertyInfo("Rail", "setup", use_need=True)
PropertyInfo("Group", "setup", use_need=True)
PropertyInfo("ClippingGroup", "setup", default_description="Objects in this group are always clipped together.")
PropertyInfo("MercatorTransform", "setup", use_need=True, default_description="The object can use mercator projection for placement.")
PropertyInfo("GeneralPos", "setup", use_need=True)
PropertyInfo("Camera", "setup", use_need=True)
PropertyInfo("DemoCast", "setup", use_need=True, default_description="The object takes part in the cutscene.")
PropertyInfo("MarioFaceShipNpcRegister", "setup", use_need=True, default_description="This object can be registered to a Starship Mario NPC appearance event.")
PropertyInfo("AppearPowerStar", "setup", use_need=True)
PropertyInfo("BaseMtxFollower", "setup", default_description="Objects of this class can follow another BaseMtxFollowTarget object.")
PropertyInfo("BaseMtxFollowTarget", "setup", default_description="Objects of this class can be followed by another BaseMtxFollower object.")

# Talking
PropertyInfo("Message", "talking", use_need=True, default_description="The text message ID to be used. Needs to be specified in the zone's text file.")
PropertyInfo("EventFunc", "talking", use_values=True, default_description="Object-specific behavior for EventFunc event flow nodes.")
PropertyInfo("AnimeFunc", "talking", use_values=True, default_description="Object-specific behavior for AnimeFunc event flow nodes.")
PropertyInfo("KillFunc", "talking", use_values=True, default_description="Object-specific behavior for KillFunc event flow nodes.")
PropertyInfo("BranchFunc", "talking", use_values=True, default_description="Object-specific behavior for BranchFunc branch flow nodes.")

# Properties
PropertyInfo("ScoreAttack", "property")
PropertyInfo("YoshiLockOnTarget", "property", default_description="This object can be targeted by Yoshi.")
PropertyInfo("SearchTurtle", "property", default_description="Red Koopa Shells and Gold Shells home in on this object.")
PropertyInfo("MirrorActor", "property", default_description="A mirrored version of this object is created for mirror reflection setups if placed inside a MirrorArea.")
PropertyInfo("DemoSimpleCast", "property", default_description="This object will not pause its movement during cutscenes, NPC conversations, etc.")
PropertyInfo("MoveLimitCollision", "property", default_description="The object's collision binder also checks for MoveLimit collision.")

# Placeholders, will be removed later
PropertyInfo("MapPartsSeesaw1AxisRotator", "property")
PropertyInfo("MapPartsSeesaw2AxisRotator", "property")
PropertyInfo("MapPartsSeesaw2AxisRollerRotator", "property")
PropertyInfo("MapPartsFloatingForce", "property")
PropertyInfo("FloaterFloatingForceTypeNormal", "property")


def all_properties():
    return __CACHED_PROPERTY_KEYS__


# ----------------------------------------------------------------------------------------------------------------------
# Occurrence helpers

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


def default_occurrence_field_value(key: str):
    return __FIELD_DEFAULT_VALUES__[key] if key in __FIELD_DEFAULT_VALUES__ else -1


def occurrence_field_order_key():
    return __FIELD_COLUMN_ORDER__.index


# ----------------------------------------------------------------------------------------------------------------------
# JSON helpers

def _get_attr_from_dict_(data: dict, attr_type: type, key: str, default):
    if key not in data:
        return default
    result = data[key]
    if type(result) != attr_type:
        return default
    return result


def get_str(data: dict, key: str, default: str = "") -> str:
    return _get_attr_from_dict_(data, str, key, default)


def get_int(data: dict, key: str, default: int = 0) -> int:
    return _get_attr_from_dict_(data, int, key, default)


def get_float(data: dict, key: str, default: float = 0.0) -> float:
    return _get_attr_from_dict_(data, float, key, default)


def get_bool(data: dict, key: str, default: bool = False) -> bool:
    return _get_attr_from_dict_(data, bool, key, default)


def get_list(data: dict, key: str, default: list = None) -> list:
    if default is None:
        default = []
    return _get_attr_from_dict_(data, list, key, default)


def get_dict(data: dict, key: str, default: dict = None) -> dict:
    if default is None:
        default = {}
    return _get_attr_from_dict_(data, dict, key, default)


def _read_json_(file_path: str) -> dict | list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file {file_path} does not exist")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json_(file_path: str, data: dict | list, indent: bool = True):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4 if indent else None, ensure_ascii=False)
