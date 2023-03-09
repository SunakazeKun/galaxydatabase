import sys
import database
import genwhitehole
import genpages
import traceback

from database import GalaxyDatabase, GalaxyObject, GalaxyConfig, GalaxyConfigProperty

try:
    import qdarkstyle
    __SUPPORTS_DARK_STYLE__ = True
except ImportError:
    __SUPPORTS_DARK_STYLE__ = False

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DatabaseEditor(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # --------------------------------------------------------------------------------------------------------------
        # Variable declarations
        self.database: GalaxyDatabase = database.load_database()
        self.category_indices = list(self.database.categories.keys())

        self.current_object_item = None
        self.current_object: GalaxyObject = None
        self.current_config_item = None
        self.current_config: GalaxyConfig = None
        self.current_property_item = None
        self.current_property: GalaxyConfigProperty = None
        self.config_index = dict()
        self.occurrence_index = dict()

        self.listObjects: QListWidget = None
        self.widgetObject: QWidget = None
        self.labelObjTitle: QLabel = None
        self.buttonGoToClassSMG1: QPushButton = None
        self.buttonGoToClassSMG2: QPushButton = None
        self.buttonGoToOccurrence: QPushButton = None
        self.labelObjName: QLabel = None
        self.labelObjNotes: QLabel = None
        self.labelObjCategory: QLabel = None
        self.labelObjProgress: QLabel = None
        self.labelObjAreaShape: QLabel = None
        self.labelObjFile: QLabel = None
        self.labelObjListSMG1: QLabel = None
        self.labelObjListSMG2: QLabel = None
        self.labelObjGames: QLabel = None
        self.textObjName: QLineEdit = None
        self.textObjNotes: QTextEdit = None
        self.comboObjCategory: QComboBox = None
        self.radioUnknown: QRadioButton = None
        self.radioKnown: QRadioButton = None
        self.radioFinished: QRadioButton = None
        self.comboObjAreaShape: QComboBox = None
        self.comboObjListSMG1: QComboBox = None
        self.comboObjListSMG2: QComboBox = None
        self.comboObjFile: QComboBox = None
        self.checkObjSMG1: QCheckBox = None
        self.checkObjSMG2: QCheckBox = None
        self.checkObjIsUnused: QCheckBox = None
        self.checkObjIsLeftover: QCheckBox = None

        self.listClasses: QListWidget = None
        self.widgetClass: QWidget = None
        self.labelClassTitle: QLabel = None
        self.labelClassNotes: QLabel = None
        self.labelClassGames: QLabel = None
        self.labelClassProgress: QLabel = None
        self.textClassNotes: QTextEdit = None
        self.checkClassSMG1: QCheckBox = None
        self.checkClassSMG2: QCheckBox = None
        self.radioClassUnknown: QRadioButton = None
        self.radioClassKnown: QRadioButton = None
        self.radioClassFinished: QRadioButton = None
        self.widgetProperties: QWidget = None
        self.listProperties: QListWidget = None
        self.buttonPropertyAdd: QPushButton = None
        self.buttonPropertyDelete: QPushButton = None

        self.widgetPropertySettings: QWidget = None
        self.labelPropertyName: QLabel = None
        self.labelPropertyType: QLabel = None
        self.labelPropertyGames: QLabel = None
        self.labelPropertyDescription: QLabel = None
        self.labelPropertyValues: QLabel = None
        self.labelPropertyExclusives: QLabel = None
        self.textPropertyName: QLineEdit = None
        self.comboPropertyType: QComboBox = None
        self.checkPropertySMG1: QCheckBox = None
        self.checkPropertySMG2: QCheckBox = None
        self.checkPropertyNeeded: QCheckBox = None
        self.textPropertyDescription: QTextEdit = None
        self.textPropertyValues: QTextEdit = None
        self.textPropertyExclusives: QTextEdit = None

        self.listOccurrences: QListWidget = None
        self.labelOccurrenceTitle: QLabel = None
        self.tableOccurrenceInfo: QTableWidget = None

        self.buttonSave: QPushButton = None
        self.tab: QTabWidget = None

        # --------------------------------------------------------------------------------------------------------------

        self.ui = uic.loadUi("assets/editor.ui", self)

        self.tableOccurrenceInfo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Populate selection boxes
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

        # Populate objects
        for key, value in self.database.objects.items():
            item = QListWidgetItem(key)
            item.setData(Qt.UserRole, key)
            self.set_item_color(item, value.progress)
            self.listObjects.addItem(item)

        # Populate configs
        for key, value in self.database.configs.items():
            item = QListWidgetItem(key)
            item.setData(Qt.UserRole, key)
            self.set_item_color(item, value.progress)
            self.listClasses.addItem(item)
            self.config_index[key] = item

        # Populate occurrences
        for key in self.database.occurrences.keys():
            item = QListWidgetItem(key)
            item.setData(Qt.UserRole, key)
            self.listOccurrences.addItem(item)
            self.occurrence_index[key] = item

        # Register actions
        self.buttonSave.clicked.connect(self.save_all)
        self.listOccurrences.currentItemChanged.connect(lambda i, _: self.load_occurrence(i))

        self.register_object_events()
        self.register_config_events()
        self.register_property_events()

        self.set_object_components_enabled(False)
        self.set_config_components_enabled(False)

    def register_object_events(self):
        self.listObjects.currentItemChanged.connect(lambda i, _: self.load_object(i))

        self.textObjName.textEdited.connect(self.set_object_name)
        self.textObjNotes.textChanged.connect(self.set_object_notes)
        self.comboObjCategory.currentIndexChanged.connect(self.set_object_category)
        self.radioUnknown.toggled.connect(self.set_object_progress)
        self.radioKnown.toggled.connect(self.set_object_progress)
        self.radioFinished.toggled.connect(self.set_object_progress)

        self.comboObjAreaShape.currentIndexChanged.connect(self.set_object_area_shape)
        self.comboObjListSMG1.currentIndexChanged.connect(self.set_object_list_smg1)
        self.comboObjListSMG2.currentIndexChanged.connect(self.set_object_list_smg2)
        self.comboObjFile.currentIndexChanged.connect(self.set_object_file)
        self.checkObjSMG1.stateChanged.connect(lambda s: self.set_object_game(1, s == 2))
        self.checkObjSMG2.stateChanged.connect(lambda s: self.set_object_game(2, s == 2))

        self.checkObjIsUnused.stateChanged.connect(lambda s: self.set_object_is_unused(s == 2))
        self.checkObjIsLeftover.stateChanged.connect(lambda s: self.set_object_is_leftover(s == 2))

        self.buttonGoToClassSMG1.clicked.connect(lambda: self.go_to_config(True))
        self.buttonGoToClassSMG2.clicked.connect(lambda: self.go_to_config(False))
        self.buttonGoToOccurrence.clicked.connect(self.go_to_occurrence)

    def register_config_events(self):
        self.listClasses.currentItemChanged.connect(lambda i, _: self.load_config(i))

        self.textClassNotes.textChanged.connect(self.set_config_notes)
        self.checkClassSMG1.stateChanged.connect(lambda s: self.set_config_game(1, s == 2))
        self.checkClassSMG2.stateChanged.connect(lambda s: self.set_config_game(2, s == 2))
        self.radioClassUnknown.toggled.connect(self.set_config_progress)
        self.radioClassKnown.toggled.connect(self.set_config_progress)
        self.radioClassFinished.toggled.connect(self.set_config_progress)

    def register_property_events(self):
        self.listProperties.currentItemChanged.connect(lambda i, _: self.load_property(i))
        self.buttonPropertyAdd.clicked.connect(self.try_add_property)
        self.buttonPropertyDelete.clicked.connect(self.try_delete_property)

        self.textPropertyName.textEdited.connect(self.set_property_name)
        self.comboPropertyType.currentIndexChanged.connect(self.set_property_type)
        self.checkPropertySMG1.stateChanged.connect(lambda s: self.set_property_game(1, s == 2))
        self.checkPropertySMG2.stateChanged.connect(lambda s: self.set_property_game(2, s == 2))
        self.checkPropertyNeeded.stateChanged.connect(lambda s: self.set_property_needed(s == 2))
        self.textPropertyDescription.textChanged.connect(self.set_property_description)
        self.textPropertyValues.textChanged.connect(self.set_property_values)
        self.textPropertyExclusives.textChanged.connect(self.set_property_exclusives)

    # ------------------------------------------------------------------------------------------------------------------
    # General helpers
    # ------------------------------------------------------------------------------------------------------------------
    def show_info(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Super Mario Galaxy Object Database Editor")
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def set_item_color(self, item: QListWidgetItem, progress: int):
        if progress == 2:
            item.setForeground(QColor("#008000"))
        elif progress == 1:
            item.setForeground(QColor("#FF8000"))
        else:
            item.setForeground(QColor("#FF0000"))

    def save_all(self):
        try:
            self.database.save_all()
        except:
            print(traceback.format_exc())
            return

        try:
            genwhitehole.generate_whitehole_xml(self.database)
        except:
            print(traceback.format_exc())

        try:
            genpages.generate_docs(self.database, False)
        except:
            print(traceback.format_exc())

    def _set_components_enabled_and_unblock_signals_(self, components: list, state: bool):
        for component in components:
            component.blockSignals(not state)
            component.setEnabled(state)

    def set_object_components_enabled(self, state: bool):
        components = [
            self.widgetObject,
            self.labelObjTitle,
            self.buttonGoToClassSMG1,
            self.buttonGoToClassSMG2,
            self.buttonGoToOccurrence,
            self.labelObjName,
            self.labelObjNotes,
            self.labelObjCategory,
            self.labelObjProgress,
            self.labelObjAreaShape,
            self.labelObjFile,
            self.labelObjListSMG1,
            self.labelObjListSMG2,
            self.labelObjGames,
            self.textObjName,
            self.textObjNotes,
            self.comboObjCategory,
            self.radioUnknown,
            self.radioKnown,
            self.radioFinished,
            self.comboObjAreaShape,
            self.comboObjFile,
            self.comboObjListSMG1,
            self.comboObjListSMG2,
            self.checkObjSMG1,
            self.checkObjSMG2,
            self.checkObjIsUnused,
            self.checkObjIsLeftover
        ]
        self._set_components_enabled_and_unblock_signals_(components, state)

    def set_config_components_enabled(self, state: bool):
        components = [
            self.widgetClass,
            self.labelClassTitle,
            self.labelClassNotes,
            self.labelClassGames,
            self.labelClassProgress,
            self.textClassNotes,
            self.checkClassSMG1,
            self.checkClassSMG2,
            self.radioClassUnknown,
            self.radioClassKnown,
            self.radioFinished,
            self.widgetProperties,
            self.listProperties,
            self.buttonPropertyAdd,
            self.buttonPropertyDelete
        ]
        self._set_components_enabled_and_unblock_signals_(components, state)

        if not state:
            self.set_property_components_enabled(False)

    def set_property_components_enabled(self, state: bool):
        components = [
            self.widgetPropertySettings,
            self.labelPropertyName,
            self.labelPropertyType,
            self.labelPropertyGames,
            self.labelPropertyDescription,
            self.labelPropertyValues,
            self.labelPropertyExclusives,
            self.textPropertyName,
            self.comboPropertyType,
            self.checkPropertySMG1,
            self.checkPropertySMG2,
            self.checkPropertyNeeded,
            self.textPropertyDescription,
            self.textPropertyValues,
            self.textPropertyExclusives
        ]
        self._set_components_enabled_and_unblock_signals_(components, state)

    # ------------------------------------------------------------------------------------------------------------------
    # Object events
    # ------------------------------------------------------------------------------------------------------------------
    def set_object_name(self, name: str):
        self.current_object.name = name

    def set_object_notes(self):
        self.current_object.notes = self.textObjNotes.toPlainText()

    def set_object_category(self, index: int):
        self.current_object.category = self.category_indices[index]

    def set_object_area_shape(self, index: int):
        self.current_object.area_shape = database.AREA_SHAPES[index]

    def set_object_list_smg1(self, index: int):
        self.current_object.list_smg1 = database.OBJECT_LISTS[index]

    def set_object_list_smg2(self, index: int):
        self.current_object.list_smg2 = database.OBJECT_LISTS[index]

    def set_object_file(self, index: int):
        self.current_object.file = database.OBJECT_ARCHIVES[index]

    def set_object_game(self, game: int, state: bool):
        if state:
            self.current_object.games |= (1 << (game - 1))
        else:
            self.current_object.games &= ~(1 << (game - 1))

    def set_object_progress(self):
        if self.radioFinished.isChecked():
            self.current_object.progress = 2
        elif self.radioKnown.isChecked():
            self.current_object.progress = 1
        else:
            self.current_object.progress = 0

        self.set_item_color(self.current_object_item, self.current_object.progress)

    def set_object_is_unused(self, state: bool):
        self.current_object.is_unused = state

    def set_object_is_leftover(self, state: bool):
        self.current_object.is_leftover = state

    def go_to_config(self, is_smg1: bool):
        config_name = self.current_object.config_name_smg1 if is_smg1 else self.current_object.config_name_smg2

        if config_name in self.config_index:
            item = self.config_index[config_name]
            self.listClasses.setCurrentItem(item)
            self.tab.setCurrentIndex(1)
        else:
            self.show_info(f"Could not find config information for {config_name}!")

    def go_to_occurrence(self):
        key = self.current_object_item.data(Qt.UserRole)

        if key in self.occurrence_index:
            item = self.occurrence_index[key]
            self.listOccurrences.setCurrentItem(item)
            self.tab.setCurrentIndex(2)
        else:
            self.show_info(f"Could not find occurrences for {key}!")

    # ------------------------------------------------------------------------------------------------------------------
    # Config events
    # ------------------------------------------------------------------------------------------------------------------
    def set_config_notes(self):
        self.current_config.notes = self.textClassNotes.toPlainText()

    def set_config_game(self, game: int, state: bool):
        if state:
            self.current_config.games |= (1 << (game - 1))
        else:
            self.current_config.games &= ~(1 << (game - 1))

    def set_config_progress(self):
        if self.radioClassFinished.isChecked():
            self.current_config.progress = 2
        elif self.radioClassKnown.isChecked():
            self.current_config.progress = 1
        else:
            self.current_config.progress = 0

        self.set_item_color(self.current_config_item, self.current_config.progress)

    # ------------------------------------------------------------------------------------------------------------------
    # Property events
    # ------------------------------------------------------------------------------------------------------------------
    def set_property_name(self, name: str):
        self.current_property.name = name

    def set_property_type(self, index: int):
        self.current_property.type = database.PROPERTY_TYPES[index]

    def set_property_game(self, game: int, state: bool):
        if state:
            self.current_property.games |= (1 << (game - 1))
        else:
            self.current_property.games &= ~(1 << (game - 1))

    def set_property_needed(self, state: bool):
        self.current_property.needed = state

    def set_property_description(self):
        self.current_property.description = self.textPropertyDescription.toPlainText()

    def set_property_values(self):
        all_text = self.textPropertyValues.toPlainText().strip("\r")
        self.current_property.values.clear()

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

                self.current_property.values.append({"Value": value, "Notes": desc})

    def set_property_exclusives(self):
        all_text = self.textPropertyExclusives.toPlainText().strip("\r")
        self.current_property.exclusives = all_text.split("\n") if len(all_text) else []

    # ------------------------------------------------------------------------------------------------------------------
    # Objects and class data population
    # ------------------------------------------------------------------------------------------------------------------
    def load_object(self, item: QListWidgetItem):
        self.set_object_components_enabled(False)

        if item is None:
            self.current_object_item = None
            self.current_object = None
            return

        key = item.data(Qt.UserRole)

        self.current_object_item = item
        self.current_object = self.database.objects[key]

        self.labelObjTitle.setText(self.current_object.internal_name)
        self.textObjName.setText(self.current_object.name)
        self.textObjNotes.setText(self.current_object.notes)
        self.comboObjCategory.setCurrentIndex(self.category_indices.index(self.current_object.category))

        self.comboObjAreaShape.setCurrentIndex(database.AREA_SHAPES.index(self.current_object.area_shape))
        self.comboObjListSMG1.setCurrentIndex(database.OBJECT_LISTS.index(self.current_object.list_smg1))
        self.comboObjListSMG2.setCurrentIndex(database.OBJECT_LISTS.index(self.current_object.list_smg2))
        self.comboObjFile.setCurrentIndex(database.OBJECT_ARCHIVES.index(self.current_object.file))
        self.checkObjSMG1.setChecked(bool(self.current_object.games & 1))
        self.checkObjSMG2.setChecked(bool(self.current_object.games & 2))

        self.checkObjIsUnused.setChecked(self.current_object.is_unused)
        self.checkObjIsLeftover.setChecked(self.current_object.is_leftover)

        if self.current_object.progress == 2:
            self.radioFinished.setChecked(True)
        elif self.current_object.progress == 1:
            self.radioKnown.setChecked(True)
        else:
            self.radioUnknown.setChecked(True)

        self.set_object_components_enabled(True)

    def load_config(self, item: QListWidgetItem):
        self.set_config_components_enabled(False)
        self.listProperties.clear()

        if item is None:
            self.current_config_item = None
            self.current_config = None
            return

        key = item.data(Qt.UserRole)

        self.current_config_item = item
        self.current_config = self.database.configs[key]

        self.labelClassTitle.setText(self.current_config.internal_name)
        self.textClassNotes.setText(self.current_config.notes)
        self.checkClassSMG1.setChecked(bool(self.current_config.games & 1))
        self.checkClassSMG2.setChecked(bool(self.current_config.games & 2))

        if self.current_config.progress == 1:
            self.radioClassKnown.setChecked(True)
        elif self.current_config.progress == 2:
            self.radioClassFinished.setChecked(True)
        else:
            self.radioClassUnknown.setChecked(True)

        for key in self.current_config.properties:
            item = QListWidgetItem(key)
            item.setData(Qt.UserRole, key)
            self.listProperties.addItem(item)

        self.set_config_components_enabled(True)

    def load_property(self, item: QListWidgetItem):
        self.set_property_components_enabled(False)

        if item is None:
            self.current_property_item = None
            self.current_property = None
            self.widgetPropertySettings.setEnabled(False)
            return

        key = item.data(Qt.UserRole)
        self.current_property_item = item
        self.current_property = self.current_config.properties[key]
        self.textPropertyValues.blockSignals(True)
        self.textPropertyExclusives.blockSignals(True)
        self.comboPropertyType.blockSignals(True)

        property_info = database.get_property_info(key)

        self.textPropertyName.setText(self.current_property.name)
        self.comboPropertyType.setCurrentIndex(database.PROPERTY_TYPES.index(self.current_property.type))
        self.checkPropertySMG1.setChecked(bool(self.current_property.games & 1))
        self.checkPropertySMG2.setChecked(bool(self.current_property.games & 2))
        self.textPropertyDescription.setText(self.current_property.description)
        self.textPropertyExclusives.setText("\n".join(self.current_property.exclusives))

        self.checkPropertyNeeded.setChecked(self.current_property.needed)

        text = ""
        for value_info in self.current_property.values:
            value = value_info["Value"]
            desc = value_info["Notes"]
            if len(text):
                text += "\n"
            text += f"{value} {desc}"
        self.textPropertyValues.setText(text)

        self.set_property_components_enabled(True)

        self.labelPropertyName.setEnabled(property_info.use_name)
        self.textPropertyName.setEnabled(property_info.use_name)
        self.labelPropertyType.setEnabled(property_info.use_type)
        self.comboPropertyType.setEnabled(property_info.use_type)
        self.labelPropertyValues.setEnabled(property_info.use_values)
        self.textPropertyValues.setEnabled(property_info.use_values)
        self.checkPropertyNeeded.setEnabled(property_info.use_need)

    def try_add_property(self):
        # Get list of remaining properties that can be added
        properties = list(database.all_properties())

        for key in self.current_config.properties.keys():
            if key in properties:
                properties.remove(key)

        # Select property name
        prop_name, valid = QInputDialog.getItem(self, "Select property", "Properties:", properties, editable=False)

        if valid:
            config_property = GalaxyConfigProperty(prop_name)
            self.current_config.properties[prop_name] = config_property

            item = QListWidgetItem(prop_name)
            item.setData(Qt.UserRole, prop_name)
            self.listProperties.addItem(item)

            self.listProperties.setCurrentItem(item)

    def try_delete_property(self):
        if self.current_property_item is None:
            return

        key = self.current_property_item.data(Qt.UserRole)

        if key in self.current_config.properties:
            del self.current_config.properties[key]

        self.listProperties.takeItem(self.listProperties.currentRow())
        self.current_property_item = None

    def load_occurrence(self, item: QListWidgetItem):
        if item is None:
            return

        key = item.data(Qt.UserRole)
        data = self.database.occurrences[key]
        self.tableOccurrenceInfo.clearContents()
        self.labelOccurrenceTitle.setText(f"Occurrences of {key}")

        # Collect columns
        column_names = list()

        for entry in data:
            for column in entry.keys():
                if column not in column_names:
                    column_names.append(column)

        column_names.sort(key=database.occurrence_field_order_key())

        # Shape table
        self.tableOccurrenceInfo.setColumnCount(len(column_names))
        self.tableOccurrenceInfo.setRowCount(len(data))
        self.tableOccurrenceInfo.setHorizontalHeaderLabels(column_names)

        for y, entry in enumerate(data):
            for x, column in enumerate(column_names):
                value = str(entry[column] if column in entry else database.default_occurrence_field_value(column))
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
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, trace):
        formatted = "".join(traceback.format_exception(exctype, value, trace))
        print(formatted, file=sys.stderr)
        sys.exit(1)

    sys.excepthook = exception_hook

    editor = DatabaseEditor()
    editor.setVisible(True)
    sys.exit(app.exec_())
