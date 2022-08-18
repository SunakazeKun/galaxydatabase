import sys
import database
import genwhitehole
import genpages
import traceback

try:
    import qdarkstyle
    __SUPPORTS_DARK_STYLE__ = True
except ImportError:
    __SUPPORTS_DARK_STYLE__ = False

from PyQt5 import uic, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DatabaseEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("assets/editor.ui", self)
        self.database = database.load_database()
        self.category_indices = list(self.database.categories.keys())

        self.current_object_item = None
        self.current_object = None
        self.current_class_item = None
        self.current_class = None
        self.current_property_item = None
        self.current_property = None
        self.class_index = dict()
        self.occurrence_index = dict()

        self.tableOccurrenceInfo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.widgetObject.setEnabled(False)
        self.widgetClass.setEnabled(False)

        for key, value in self.database.categories.items():
            self.comboObjCategory.addItem(value)
        for line in database.AREA_SHAPES:
            self.comboObjAreaShape.addItem(line)
        for line in database.OBJECT_LISTS:
            self.comboObjListSMG1.addItem(line)
            self.comboObjListSMG2.addItem(line)
        for line in database.OBJECT_ARCHIVES:
            self.comboObjFile.addItem(line)
        for line in database.PROPERTY_TYPES:
            self.comboPropertyType.addItem(line)

        for key, value in self.database.objects.items():
            item = QListWidgetItem(key)
            item.setData(QtCore.Qt.UserRole, key)
            self.set_item_color(item, False)
            self.listObjects.addItem(item)

        for key, value in self.database.classes.items():
            item = QListWidgetItem(key)
            item.setData(QtCore.Qt.UserRole, key)
            self.set_item_color(item, True)
            self.listClasses.addItem(item)
            self.class_index[key] = item

        for key in self.database.occurrences.keys():
            item = QListWidgetItem(key)
            item.setData(QtCore.Qt.UserRole, key)
            self.listOccurrences.addItem(item)
            self.occurrence_index[key] = item

        # Register actions
        self.buttonSave.clicked.connect(self.save_all)
        self.listOccurrences.currentItemChanged.connect(lambda i, _: self.load_occurrence(i))
        self.register_object_events()
        self.register_class_events()
        self.register_property_events()

    def show_info(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Super Mario Galaxy Object Database Editor")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    # ------------------------------------------------------------------------------------------------------------------
    # Manipulation events
    # ------------------------------------------------------------------------------------------------------------------
    def register_object_events(self):
        self.listObjects.currentItemChanged.connect(lambda i, _: self.load_object(i))

        self.textObjName.textEdited.connect(lambda s: self.set_obj_attr("Name", s))
        self.textObjNotes.textChanged.connect(lambda: self.set_obj_attr("Notes", self.textObjNotes.toPlainText()))
        self.comboObjCategory.currentIndexChanged.connect(lambda i: self.set_obj_attr("Category", self.category_indices[i]))
        self.radioUnknown.toggled.connect(lambda s: self.set_obj_attr("Progress", 0))
        self.radioKnown.toggled.connect(lambda s: self.set_obj_attr("Progress", 1))
        self.radioFinished.toggled.connect(lambda s: self.set_obj_attr("Progress", 2))

        self.comboObjAreaShape.currentIndexChanged.connect(lambda i: self.set_obj_attr("AreaShape", database.AREA_SHAPES[i]))
        self.comboObjListSMG1.currentIndexChanged.connect(lambda i: self.set_obj_attr("ListSMG1", database.OBJECT_LISTS[i]))
        self.comboObjListSMG2.currentIndexChanged.connect(lambda i: self.set_obj_attr("ListSMG2", database.OBJECT_LISTS[i]))
        self.comboObjFile.currentIndexChanged.connect(lambda i: self.set_obj_attr("File", database.OBJECT_ARCHIVES[i]))
        self.checkObjSMG1.stateChanged.connect(lambda s: self.toggle_obj_mask("Games", 1, s == 2))
        self.checkObjSMG2.stateChanged.connect(lambda s: self.toggle_obj_mask("Games", 2, s == 2))

        self.checkObjIsUnused.stateChanged.connect(lambda s: self.set_obj_attr("IsUnused", s == 2))
        self.checkObjIsLeftover.stateChanged.connect(lambda s: self.set_obj_attr("IsLeftover", s == 2))

        self.buttonGoToClassSMG1.clicked.connect(lambda: self.go_to_class(True))
        self.buttonGoToClassSMG2.clicked.connect(lambda: self.go_to_class(False))
        self.buttonGoToOccurrence.clicked.connect(self.go_to_occurrence)

    def register_class_events(self):
        self.listClasses.currentItemChanged.connect(lambda i, _: self.load_class(i))

        self.textClassNotes.textChanged.connect(lambda: self.set_class_attr("Notes", self.textClassNotes.toPlainText()))
        self.checkClassSMG1.stateChanged.connect(lambda s: self.toggle_class_mask("Games", 1, s == 2))
        self.checkClassSMG2.stateChanged.connect(lambda s: self.toggle_class_mask("Games", 2, s == 2))
        self.radioClassUnknown.toggled.connect(lambda s: self.set_class_attr("Progress", 0))
        self.radioClassKnown.toggled.connect(lambda s: self.set_class_attr("Progress", 1))
        self.radioClassFinished.toggled.connect(lambda s: self.set_class_attr("Progress", 2))

    def register_property_events(self):
        self.listProperties.currentItemChanged.connect(lambda i, _: self.load_property(i))
        self.buttonPropertyAdd.clicked.connect(self.try_add_property)
        self.buttonPropertyDelete.clicked.connect(self.try_delete_property)

        self.textPropertyName.textEdited.connect(lambda s: self.set_property_attr("Name", s))
        self.comboPropertyType.currentIndexChanged.connect(lambda i: self.set_property_attr("Type", database.PROPERTY_TYPES[i]))
        self.checkPropertySMG1.stateChanged.connect(lambda s: self.toggle_property_mask("Games", 1, s == 2))
        self.checkPropertySMG2.stateChanged.connect(lambda s: self.toggle_property_mask("Games", 2, s == 2))
        self.checkPropertyNeeded.stateChanged.connect(lambda s: self.set_property_attr("Needed", s == 2))
        self.textPropertyDescription.textChanged.connect(lambda: self.set_property_attr("Description", self.textPropertyDescription.toPlainText()))
        self.textPropertyValues.textChanged.connect(self.set_property_values)
        self.textPropertyExclusives.textChanged.connect(self.set_property_exclusives)

    def save_all(self):
        self.database.save_all()

        # This is to find errors with the generator functions. If they fail, tell the user about it in the console. This
        # prevents a hard crash that may cause data loss. This is a temporary solution, though.
        try:
            genwhitehole.generate(self.database)
        except Exception:
            print(traceback.format_exc())

        try:
            genpages.generate(self.database, False)
        except Exception:
            print(traceback.format_exc())

    def go_to_class(self, is_smg1: bool):
        key = self.current_object_item.data(QtCore.Qt.UserRole)
        class_key = "ClassNameSMG1" if is_smg1 else "ClassNameSMG2"
        class_name = self.database.objects[key][class_key]

        if class_name in self.class_index:
            item = self.class_index[class_name]
            self.listClasses.setCurrentItem(item)
            self.tab.setCurrentIndex(1)
        else:
            self.show_info(f"Could not find class information for {class_name}!")

    def go_to_occurrence(self):
        key = self.current_object_item.data(QtCore.Qt.UserRole)

        if key in self.occurrence_index:
            item = self.occurrence_index[key]
            self.listOccurrences.setCurrentItem(item)
            self.tab.setCurrentIndex(2)
        else:
            self.show_info(f"Could not find occurrences for {key}!")

    def set_obj_attr(self, key, val):
        self.current_object[key] = val

        if key == "Progress":
            self.set_item_color(self.current_object_item, False)

    def toggle_obj_mask(self, key, val, state):
        if state:
            self.current_object[key] |= val
        else:
            self.current_object[key] &= ~val

    def set_class_attr(self, key, val):
        self.current_class[key] = val

        if key == "Progress":
            self.set_item_color(self.current_class_item, True)

    def toggle_class_mask(self, key, val, state):
        if state:
            self.current_class[key] |= val
        else:
            self.current_class[key] &= ~val

    def set_property_attr(self, key, val):
        self.current_property[key] = val

    def toggle_property_mask(self, key, val, state):
        if state:
            self.current_property[key] |= val
        else:
            self.current_property[key] &= ~val

    def set_property_values(self):
        all_text = self.textPropertyValues.toPlainText().strip("\r")
        self.current_property["Values"].clear()

        if len(all_text):
            for line in all_text.split("\n"):
                line = line.lstrip(" \t").rstrip(" \t")

                if len(line) == 0:
                    continue

                split = line.split(" ", 1)

                if len(split) == 1:
                    value = line
                    desc = ""
                else:
                    value = split[0]
                    desc = split[1]

                self.current_property["Values"].append({"Value": value, "Notes": desc})

    def set_property_exclusives(self):
        all_text = self.textPropertyExclusives.toPlainText().strip("\r")
        self.current_property["Exclusives"] = all_text.split("\n") if len(all_text) else list()

    def set_item_color(self, item: QListWidgetItem, is_class: bool):
        key = item.data(QtCore.Qt.UserRole)
        data = self.database.classes[key] if is_class else self.database.objects[key]

        if data["Progress"] == 2:
            item.setForeground(QColor("#008000"))
        elif data["Progress"] == 1:
            item.setForeground(QColor("#FF8000"))
        else:
            item.setForeground(QColor("#FF0000"))

    # ------------------------------------------------------------------------------------------------------------------
    # Objects and class data population
    # ------------------------------------------------------------------------------------------------------------------
    def load_object(self, item: QListWidgetItem):
        if item is None:
            self.current_object_item = None
            self.current_object = None
            self.widgetObject.setEnabled(False)
            return

        key = item.data(QtCore.Qt.UserRole)
        data = self.database.objects[key]
        self.current_object_item = item
        self.current_object = data
        self.textObjNotes.blockSignals(True)

        self.labelObjTitle.setText(f"{data['InternalName']}")
        self.textObjName.setText(data["Name"])
        self.textObjNotes.setText(data["Notes"])
        self.comboObjCategory.setCurrentIndex(self.category_indices.index(data["Category"]))

        self.comboObjAreaShape.setCurrentIndex(database.AREA_SHAPES.index(data["AreaShape"]))
        self.comboObjListSMG1.setCurrentIndex(database.OBJECT_LISTS.index(data["ListSMG1"]))
        self.comboObjListSMG2.setCurrentIndex(database.OBJECT_LISTS.index(data["ListSMG2"]))
        self.comboObjFile.setCurrentIndex(database.OBJECT_ARCHIVES.index(data["File"]))
        self.checkObjSMG1.setChecked(bool(data["Games"] & 1))
        self.checkObjSMG2.setChecked(bool(data["Games"] & 2))

        self.checkObjIsUnused.setChecked(data["IsUnused"])
        self.checkObjIsLeftover.setChecked(data["IsLeftover"])

        if data["Progress"] == 2:
            self.radioFinished.setChecked(True)
        elif data["Progress"] == 1:
            self.radioKnown.setChecked(True)
        else:
            self.radioUnknown.setChecked(True)

        self.textObjNotes.blockSignals(False)
        self.widgetObject.setEnabled(True)

    def load_class(self, item: QListWidgetItem):
        self.widgetPropertySettings.setEnabled(False)
        self.listProperties.clear()

        if item is None:
            self.current_class_item = None
            self.current_class = None
            self.widgetClass.setEnabled(False)
            return

        key = item.data(QtCore.Qt.UserRole)
        data = self.database.classes[key]
        self.current_class_item = item
        self.current_class = data
        self.textClassNotes.blockSignals(True)

        self.labelClassTitle.setText(f"{data['InternalName']}")
        self.textClassNotes.setText(data["Notes"])
        self.checkClassSMG1.setChecked(data["Games"] & 1)
        self.checkClassSMG2.setChecked(data["Games"] & 2)

        if data["Progress"] == 1:
            self.radioClassKnown.setChecked(True)
        elif data["Progress"] == 2:
            self.radioClassFinished.setChecked(True)
        else:
            self.radioClassUnknown.setChecked(True)

        for key in data["Parameters"]:
            item = QListWidgetItem(key)
            item.setData(QtCore.Qt.UserRole, key)
            self.listProperties.addItem(item)

        self.textClassNotes.blockSignals(False)
        self.widgetClass.setEnabled(True)

    def load_property(self, item: QListWidgetItem):
        if item is None:
            self.current_property_item = None
            self.current_property = None
            self.widgetPropertySettings.setEnabled(False)
            return

        key = item.data(QtCore.Qt.UserRole)
        data = self.current_class["Parameters"][key]
        self.current_property_item = item
        self.current_property = data
        self.textPropertyValues.blockSignals(True)
        self.textPropertyExclusives.blockSignals(True)
        self.comboPropertyType.blockSignals(True)

        enable_name, enable_type, enable_desc, enable_values = database.property_info(key)
        self.labelPropertyName.setEnabled(enable_name)
        self.textPropertyName.setEnabled(enable_name)
        self.labelPropertyType.setEnabled(enable_type)
        self.comboPropertyType.setEnabled(enable_type)
        self.labelPropertyDescription.setEnabled(enable_desc)
        self.textPropertyDescription.setEnabled(enable_desc)
        self.labelPropertyValues.setEnabled(enable_values)
        self.textPropertyValues.setEnabled(enable_values)

        self.textPropertyName.setText(data["Name"] if enable_name else "")
        self.comboPropertyType.setCurrentIndex(database.PROPERTY_TYPES.index(data["Type"]) if enable_type else 0)
        self.checkPropertySMG1.setChecked(data["Games"] & 1)
        self.checkPropertySMG2.setChecked(data["Games"] & 2)
        self.checkPropertyNeeded.setChecked(data["Needed"])
        self.textPropertyDescription.setText(data["Description"] if enable_desc else "")
        self.textPropertyExclusives.setText("\n".join(data["Exclusives"]))

        if enable_values:
            text = ""
            for value_info in data["Values"]:
                value = value_info["Value"]
                desc = value_info["Notes"]
                if len(text):
                    text += "\n"
                text += f"{value} {desc}"
            self.textPropertyValues.setText(text)
        else:
            self.textPropertyValues.setText("")

        self.textPropertyValues.blockSignals(False)
        self.textPropertyExclusives.blockSignals(False)
        self.comboPropertyType.blockSignals(False)

        self.widgetPropertySettings.setEnabled(True)

    def try_add_property(self):
        # Get list of remaining properties that can be specified
        properties = list(database.all_properties())

        for key in self.current_class["Parameters"].keys():
            if key in properties:
                properties.remove(key)

        # Select new property
        newprop, valid = QInputDialog.getItem(self, "Select property to add", "Properties:", properties, editable=False)

        if valid:
            enable_name, enable_type, enable_desc, enable_values = database.property_info(newprop)

            # Some properties are not always needed to save space
            data = dict()
            if enable_name:
                data["Name"] = ""
            if enable_type:
                data["Type"] = "Integer"
            data["Games"] = 0
            data["Needed"] = False
            if enable_desc:
                data["Description"] = database.default_field_description(newprop)
            if enable_values:
                data["Values"] = list()
            data["Exclusives"] = list()

            # Register data, create list item and select it
            self.current_class["Parameters"][newprop] = data
            item = QListWidgetItem(newprop)
            item.setData(QtCore.Qt.UserRole, newprop)
            self.listProperties.addItem(item)
            self.listProperties.setCurrentItem(item)

    def try_delete_property(self):
        if self.current_property_item is None:
            return

        key = self.current_property_item.data(QtCore.Qt.UserRole)

        if key in self.current_class["Parameters"]:
            del self.current_class["Parameters"][key]

        self.listProperties.takeItem(self.listProperties.currentRow())

    def load_occurrence(self, item: QListWidgetItem):
        if item is None:
            return

        key = item.data(QtCore.Qt.UserRole)
        data = self.database.occurrences[key]
        self.tableOccurrenceInfo.clearContents()
        self.labelOccurrenceTitle.setText(f"Occurrences of {key}")

        # Collect columns
        column_names = list()

        for entry in data:
            for column in entry.keys():
                if column not in column_names:
                    column_names.append(column)

        column_names.sort(key=database.FIELD_COLUMN_ORDER)

        # Shape table
        self.tableOccurrenceInfo.setColumnCount(len(column_names))
        self.tableOccurrenceInfo.setRowCount(len(data))
        self.tableOccurrenceInfo.setHorizontalHeaderLabels(column_names)

        for y, entry in enumerate(data):
            for x, column in enumerate(column_names):
                value = str(entry[column] if column in entry else database.default_field_value(column))
                self.tableOccurrenceInfo.setItem(y, x, QTableWidgetItem(value))


# ----------------------------------------------------------------------------------------------------------------------
# Main entry point for Qt application
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("assets/icon.png"))

    if __SUPPORTS_DARK_STYLE__:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Setup exception hook
    old_excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        old_excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    editor = DatabaseEditor()
    editor.setVisible(True)
    sys.exit(app.exec_())
