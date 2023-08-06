import os

from PySide import QtGui, QtCore

import asphodel

from .ui_preferences import Ui_PreferencesDialog


# NOTE: code can only display one alternate unit per unit type in the dialog
alternate_units = [{"unit_type": asphodel.UNIT_TYPE_WATT,
                    "setting_name": "UseHorsepower",
                    "scale": 1 / 746.0,
                    "offset": 0.0,
                    "unit_strings": ("HP", "HP", "HP")},
                   {"unit_type": asphodel.UNIT_TYPE_M_PER_S2,
                    "setting_name": "UseGForce",
                    "scale": 1 / 9.80665,
                    "offset": 0.0,
                    "unit_strings": ("g", "g", "<b>g</b>")},
                   {"unit_type": asphodel.UNIT_TYPE_HZ,
                    "setting_name": "UseCPM",
                    "scale": 60.0,
                    "offset": 0.0,
                    "unit_strings": ("CPM", "CPM", "CPM")},
                   {"unit_type": asphodel.UNIT_TYPE_METER,
                    "setting_name": "UseInch",
                    "scale": 39.3700787401575,
                    "offset": 0.0,
                    "unit_strings": ("in", "in", "in")},
                   {"unit_type": asphodel.UNIT_TYPE_GRAM,
                    "setting_name": "UseOunce",
                    "scale": 0.035273961949580414,
                    "offset": 0.0,
                    "unit_strings": ("oz", "oz", "oz")},
                    {"unit_type": asphodel.UNIT_TYPE_M3_PER_S,
                    "setting_name": "UseGPM",
                    "scale": 15850.323141489,
                    "offset": 0.0,
                    "unit_strings": ("gal/min", "gal/min", "gal/min")}]


def read_bool_setting(settings, setting_name, default=False):
    try:
        s = settings.value(setting_name)
        if s is not None:
            s_int = int(s)
            return False if s_int == 0 else True
        else:
            return default
    except:
        return default


def read_int_setting(settings, setting_name, default=0):
    try:
        s = settings.value(setting_name)
        if s is not None:
            return int(s)
        else:
            return default
    except:
        return default


def write_bool_setting(settings, setting_name, value):
    settings.setValue(setting_name, 1 if value else 0)


def create_unit_formatter(settings, unit_type, minimum, maximum, resolution):
    use_mixed = read_bool_setting(settings, "UseMixed", False)
    use_metric = read_bool_setting(settings, "UseMetric", True)

    if use_mixed:
        for alternate_unit in alternate_units:
            if unit_type == alternate_unit['unit_type']:
                use_alternate = read_bool_setting(
                    settings, alternate_unit['setting_name'], False)
                if use_alternate:
                    return asphodel.nativelib.create_custom_unit_formatter(
                        alternate_unit["scale"], alternate_unit["offset"],
                        resolution, *alternate_unit["unit_strings"])

        setting_name = "UseMetricType{}".format(unit_type)
        type_metric = read_bool_setting(settings, setting_name,
                                        use_metric)
        return asphodel.nativelib.create_unit_formatter(
            unit_type, minimum, maximum, resolution, use_metric=type_metric)

    return asphodel.nativelib.create_unit_formatter(
        unit_type, minimum, maximum, resolution, use_metric=use_metric)


class PreferencesDialog(QtGui.QDialog, Ui_PreferencesDialog):
    def __init__(self, parent=None):
        # NOTE: WindowTitleHint | WindowSystemMenuHint disables "What's This"
        super().__init__(parent, QtCore.Qt.WindowTitleHint |
                         QtCore.Qt.WindowSystemMenuHint)

        self.settings = QtCore.QSettings()

        # key: unit type, value: {"group": Q button group,
        #                         "metric": button,
        #                         "us": button,
        #                         "alt": button or None,
        #                         "alt_setting": setting string or None}
        self.unit_buttons = {}

        self.setupUi(self)

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.create_unit_buttons()

        self.accepted.connect(self.write_settings)
        self.browseButton.clicked.connect(self.browse_cb)
        self.metricUnits.toggled.connect(self.toggled_metric)
        self.usUnits.toggled.connect(self.toggled_us)
        self.mixedUnits.toggled.connect(self.toggled_mixed)

        self.unitGridLayout.setColumnStretch(0, 1)
        self.unitGridLayout.setColumnStretch(1, 1)
        self.unitGridLayout.setColumnStretch(2, 1)

        self.read_settings()

    def browse_cb(self):
        base_dir = self.outputLocation.text()
        base_dir = QtGui.QFileDialog.getExistingDirectory(self, dir=base_dir)

        if base_dir:
            self.outputLocation.setText(base_dir)

    def create_unit_buttons(self):
        for unit_type_name in asphodel.unit_type_names:
            unit_type = getattr(asphodel, unit_type_name)

            metric_formatter = asphodel.nativelib.create_unit_formatter(
                unit_type, 0.0, 0.0, 0.0, use_metric=True)
            us_formatter = asphodel.nativelib.create_unit_formatter(
                unit_type, 0.0, 0.0, 0.0, use_metric=False)

            # see if there's an alternate type for this button
            alt_button = None
            alt_setting = None
            for alternate_unit in alternate_units:
                if unit_type == alternate_unit['unit_type']:
                    alt_setting = alternate_unit['setting_name']
                    alt_button = QtGui.QRadioButton(self.unitTab)
                    alt_name = alternate_unit['unit_strings'][1]  # UTF-8
                    metric_relation = metric_formatter.format_utf8(
                        1 / alternate_unit['scale'])
                    alt_text = "{} ({})".format(alt_name, metric_relation)
                    alt_button.setText(alt_text)
                    break

            if metric_formatter != us_formatter:
                # need two buttons
                row_count = self.unitGridLayout.rowCount()
                button_group = QtGui.QButtonGroup(self.unitTab)

                metric_button = QtGui.QRadioButton(self.unitTab)
                button_group.addButton(metric_button)
                metric_button.setText(metric_formatter.unit_utf8)
                self.unitGridLayout.addWidget(metric_button, row_count, 0)

                us_button = QtGui.QRadioButton(self.unitTab)
                button_group.addButton(us_button)
                us_button.setText(us_formatter.unit_utf8)
                self.unitGridLayout.addWidget(us_button, row_count, 1)

                if alt_button:
                    button_group.addButton(alt_button)
                    self.unitGridLayout.addWidget(alt_button, row_count, 2)

                button_dict = {"group": button_group,
                               "metric": metric_button,
                               "us": us_button,
                               "alt": alt_button,
                               "alt_setting": alt_setting}
                self.unit_buttons[unit_type] = button_dict
            elif alt_button is not None:
                # need a combined metric/us button
                row_count = self.unitGridLayout.rowCount()
                button_group = QtGui.QButtonGroup(self.unitTab)

                metric_us_button = QtGui.QRadioButton(self.unitTab)
                button_group.addButton(metric_us_button)
                metric_us_button.setText(metric_formatter.unit_utf8)
                self.unitGridLayout.addWidget(metric_us_button, row_count, 0,
                                              1, 2)

                if alt_button:
                    button_group.addButton(alt_button)
                    self.unitGridLayout.addWidget(alt_button, row_count, 2)

                button_dict = {"group": button_group,
                               "metric": metric_us_button,
                               "us": metric_us_button,
                               "alt": alt_button,
                               "alt_setting": alt_setting}
                self.unit_buttons[unit_type] = button_dict

    def read_settings(self):
        base_dir = self.settings.value("BasePath")
        if not base_dir:
            loc = QtGui.QDesktopServices.DocumentsLocation
            documents_path = QtGui.QDesktopServices.storageLocation(loc)
            app_name = QtGui.QApplication.applicationName()
            base_dir = os.path.join(documents_path, app_name + " Data")
        self.outputLocation.setText(base_dir)
        self.outputLocation.setCursorPosition(0)

        use_mixed = read_bool_setting(self.settings, "UseMixed", False)
        use_metric = read_bool_setting(self.settings, "UseMetric", True)

        if use_mixed:
            self.mixedUnits.setChecked(True)

            # load unit settings
            for unit_type, button_dict in self.unit_buttons.items():
                if button_dict["alt"] is not None:
                    use_alt = read_bool_setting(
                        self.settings, button_dict["alt_setting"], False)
                    if use_alt:
                        button_dict["alt"].setChecked(True)
                else:
                    use_alt = False

                if not use_alt:
                    setting_name = "UseMetricType{}".format(unit_type)
                    type_metric = read_bool_setting(
                        self.settings, setting_name, use_metric)
                    if type_metric:
                        button_dict["metric"].setChecked(True)
                    else:
                        button_dict["us"].setChecked(True)
        else:
            if use_metric:
                self.metricUnits.setChecked(True)
            else:
                self.usUnits.setChecked(True)

        auto_rgb = read_bool_setting(self.settings, "AutoRGB", True)
        self.automaticRGBCheckBox.setChecked(auto_rgb)

        downsample = read_bool_setting(self.settings, "Downsample", True)
        self.downsampleCheckBox.setChecked(downsample)

        compression_level = read_int_setting(self.settings,
                                             "CompressionLevel", 6)
        self.compressionLevel.setValue(compression_level)

        self.settings.beginGroup("Upload")
        upload_enabled = read_bool_setting(self.settings, "Enabled", False)
        self.enableUpload.setChecked(upload_enabled)
        s3_bucket = self.settings.value("S3Bucket")
        if s3_bucket:
            self.s3Bucket.setText(s3_bucket.strip())
        aws_region = self.settings.value("AWSRegion")
        if aws_region:
            self.awsRegion.setText(aws_region.strip())
        upload_directory = self.settings.value("Directory")
        if upload_directory:
            self.uploadDirectory.setText(upload_directory.strip())
        access_key_id = self.settings.value("AccessKeyID")
        if access_key_id:
            self.uploadAccessKeyID.setText(access_key_id.strip())
        secret_access_key = self.settings.value("SecretAccessKey")
        if secret_access_key:
            self.uploadSecretAccessKey.setText(secret_access_key.strip())
        delete_original = read_bool_setting(self.settings, "DeleteOriginal",
                                            False)
        self.uploadDeleteOriginal.setChecked(delete_original)
        self.settings.endGroup()

    def write_settings(self):
        base_dir = self.outputLocation.text()
        self.settings.setValue("BasePath", base_dir)

        use_mixed = self.mixedUnits.isChecked()
        write_bool_setting(self.settings, "UseMixed", use_mixed)

        if use_mixed:
            for unit_type, button_dict in self.unit_buttons.items():
                if button_dict["alt"] is not None:
                    use_alt = button_dict["alt"].isChecked()
                    write_bool_setting(self.settings,
                                       button_dict["alt_setting"], use_alt)
                else:
                    use_alt = False

                if not use_alt:
                    if button_dict["metric"] is not button_dict["us"]:
                        setting_name = "UseMetricType{}".format(unit_type)
                        type_metric = button_dict["metric"].isChecked()
                        write_bool_setting(self.settings, setting_name,
                                           type_metric)
        else:
            use_metric = self.metricUnits.isChecked()
            write_bool_setting(self.settings, "UseMetric", use_metric)

        auto_rgb = self.automaticRGBCheckBox.isChecked()
        write_bool_setting(self.settings, "AutoRGB", auto_rgb)

        downsample = self.downsampleCheckBox.isChecked()
        write_bool_setting(self.settings, "Downsample", downsample)

        compression_level = self.compressionLevel.value()
        self.settings.setValue("CompressionLevel", compression_level)

        self.settings.beginGroup("Upload")
        upload_enabled = self.enableUpload.isChecked()
        write_bool_setting(self.settings, "Enabled", upload_enabled)
        s3_bucket = self.s3Bucket.text().strip()
        self.settings.setValue("S3Bucket", s3_bucket)
        aws_region = self.awsRegion.text().strip()
        self.settings.setValue("AWSRegion", aws_region)
        upload_directory = self.uploadDirectory.text().strip()
        self.settings.setValue("Directory", upload_directory)
        access_key_id = self.uploadAccessKeyID.text().strip()
        self.settings.setValue("AccessKeyID", access_key_id)
        secret_access_key = self.uploadSecretAccessKey.text().strip()
        self.settings.setValue("SecretAccessKey", secret_access_key)
        delete_original = self.uploadDeleteOriginal.isChecked()
        write_bool_setting(self.settings, "DeleteOriginal", delete_original)
        self.settings.endGroup()

    def toggled_metric(self, junk=None):
        if self.metricUnits.isChecked():
            for button_dict in self.unit_buttons.values():
                button_dict['metric'].setChecked(True)

                button_dict['metric'].setEnabled(False)
                button_dict['us'].setEnabled(False)
                if button_dict['alt'] is not None:
                    button_dict['alt'].setEnabled(False)

    def toggled_us(self, junk=None):
        if self.usUnits.isChecked():
            for button_dict in self.unit_buttons.values():
                button_dict['us'].setChecked(True)

                button_dict['metric'].setEnabled(False)
                button_dict['us'].setEnabled(False)
                if button_dict['alt'] is not None:
                    button_dict['alt'].setEnabled(False)

    def toggled_mixed(self, junk=None):
        if self.mixedUnits.isChecked():
            for button_dict in self.unit_buttons.values():
                button_dict['metric'].setEnabled(True)
                button_dict['us'].setEnabled(True)
                if button_dict['alt'] is not None:
                    button_dict['alt'].setEnabled(True)
