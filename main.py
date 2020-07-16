from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback, sys
import numpy as np
from random import randint
import RPi.GPIO as GPIO

class WorkerSignals(QObject):
        '''
        Defines the signals available from a running worker thread.
        Supported signals are:
        - finished signal, with no data to indicate when the task is complete.
        no data

        - error signal which receives a tuple of Exception type, Exception value and formatted traceback.
        `tuple` (exctype, value, traceback.format_exc() )

        - result signal receiving any object type from the executed function.
        `object` data returned from processing, anything
        '''
        finished = pyqtSignal()
        error = pyqtSignal(tuple)
        result = pyqtSignal(object)
        res = pyqtSignal(str)
        progress = pyqtSignal(str)

class Worker(QRunnable):
        '''
        Worker thread
        Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

        :param callback: The function callback to run on this worker thread. Supplied args and 
                        kwargs will be passed through to the runner.
        :type callback: function
        :param args: Arguments to pass to the callback function
        :param kwargs: Keywords to pass to the callback function
        '''

        def __init__(self, fn, *args, **kwargs):
                super(Worker, self).__init__()
                # Store constructor arguments (re-used for processing)
                self.fn = fn
                self.args = args
                self.kwargs = kwargs
                self.signals = WorkerSignals()
                self.kwargs['progress_callback'] = self.signals.progress 

        @pyqtSlot()
        def run(self):
                '''
                Initialise the runner function with passed args, kwargs.
                '''

                # Retrieve args/kwargs here; and fire processing using them
                try:
                        result = self.fn(
                        *self.args, **self.kwargs
                        )
                except:
                        traceback.print_exc()
                        exctype, value = sys.exc_info()[:2]
                        self.signals.error.emit((exctype, value, traceback.format_exc()))
                else:
                        self.signals.result.emit(result)  # Return the result of the processing
                finally:
                        self.signals.finished.emit()  # Done

class Ui_patientSettingsWindow(QObject):
        #Initialize variables that will interact between classes
        patient_age = QtCore.pyqtSignal(int)
        patient_height = QtCore.pyqtSignal(int)
        patient_gender = QtCore.pyqtSignal(str)
        def __init__(self):
                super(Ui_patientSettingsWindow, self).__init__()
                self.signals = WorkerSignals()

        @pyqtSlot()
        def setupUi(self, patientSettingsWindow):
                """
                Setup for GUI design for this class. We set the following properties:
                        - Grids/Frames/Layouts
                        - Widgets/Lines/Labels/input boxes/Buttons (properties as colour and sizes)
                        - Font properties
                """
                patientSettingsWindow.setObjectName("patientSettingsWindow")
                patientSettingsWindow.resize(1000, 287)
                patientSettingsWindow.setWindowModality(QtCore.Qt.NonModal)
                self.centralwidget = QtWidgets.QWidget(patientSettingsWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.frame_patient_settings = QtWidgets.QFrame(self.centralwidget)
                self.frame_patient_settings.setMinimumSize(QtCore.QSize(976, 220))
                self.frame_patient_settings.setMaximumSize(QtCore.QSize(1700, 600))
                self.frame_patient_settings.setStyleSheet("background-color: rgb(164, 176, 179);")
                self.frame_patient_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_patient_settings.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_patient_settings.setObjectName("frame_patient_settings")
                self.gridLayout = QtWidgets.QGridLayout(self.frame_patient_settings)
                self.gridLayout.setObjectName("gridLayout")
                self.verticalLayout_4 = QtWidgets.QVBoxLayout()
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_14.setObjectName("horizontalLayout_14")
                spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_14.addItem(spacerItem)
                self.label_5 = QtWidgets.QLabel(self.frame_patient_settings)
                font = QtGui.QFont()
                font.setPointSize(30)
                self.label_5.setFont(font)
                self.label_5.setObjectName("label_5")
                self.horizontalLayout_14.addWidget(self.label_5)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_14.addItem(spacerItem1)
                self.verticalLayout_4.addLayout(self.horizontalLayout_14)
                self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_6.setObjectName("horizontalLayout_6")
                self.verticalLayout_25 = QtWidgets.QVBoxLayout()
                self.verticalLayout_25.setObjectName("verticalLayout_25")
                self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_5.setObjectName("horizontalLayout_5")
                self.verticalLayout_24 = QtWidgets.QVBoxLayout()
                self.verticalLayout_24.setObjectName("verticalLayout_24")
                self.label_height = QtWidgets.QLabel(self.frame_patient_settings)
                self.label_height.setMinimumSize(QtCore.QSize(100, 0))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_height.setFont(font)
                self.label_height.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.label_height.setObjectName("label_height")
                self.verticalLayout_24.addWidget(self.label_height)
                self.horizontalLayout_5.addLayout(self.verticalLayout_24)
                self.spinBox_height = QtWidgets.QSpinBox(self.frame_patient_settings)
                self.spinBox_height.setMinimumSize(QtCore.QSize(80, 35))
                font = QtGui.QFont()
                font.setPointSize(22)
                self.spinBox_height.setFont(font)
                self.spinBox_height.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                "QSpinBox::down-button { width: 32px; }")
                self.spinBox_height.setFrame(True)
                self.spinBox_height.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_height.setMinimum(20)
                self.spinBox_height.setMaximum(220)
                self.spinBox_height.setProperty("value", 160)
                self.spinBox_height.setObjectName("spinBox_height")
                self.horizontalLayout_5.addWidget(self.spinBox_height)
                self.verticalLayout_25.addLayout(self.horizontalLayout_5)
                self.horizontalSlider_height = QtWidgets.QSlider(self.frame_patient_settings)
                self.horizontalSlider_height.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSlider_height.setObjectName("horizontalSlider_height")
                self.verticalLayout_25.addWidget(self.horizontalSlider_height)
                self.horizontalLayout_6.addLayout(self.verticalLayout_25)
                self.line = QtWidgets.QFrame(self.frame_patient_settings)
                self.line.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line.setFrameShape(QtWidgets.QFrame.VLine)
                self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line.setObjectName("line")
                self.horizontalLayout_6.addWidget(self.line)
                self.verticalLayout_23 = QtWidgets.QVBoxLayout()
                self.verticalLayout_23.setObjectName("verticalLayout_23")
                self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_4.setObjectName("horizontalLayout_4")
                self.label_age = QtWidgets.QLabel(self.frame_patient_settings)
                self.label_age.setMinimumSize(QtCore.QSize(60, 0))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_age.setFont(font)
                self.label_age.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.label_age.setObjectName("label_age")
                self.horizontalLayout_4.addWidget(self.label_age)
                self.spinBox_age = QtWidgets.QSpinBox(self.frame_patient_settings)
                self.spinBox_age.setMinimumSize(QtCore.QSize(70, 35))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.spinBox_age.setFont(font)
                self.spinBox_age.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                "QSpinBox::down-button { width: 32px; }")
                self.spinBox_age.setFrame(True)
                self.spinBox_age.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_age.setMaximum(120)
                self.spinBox_age.setProperty("value", 40)
                self.spinBox_age.setObjectName("spinBox_age")
                self.horizontalLayout_4.addWidget(self.spinBox_age)
                self.verticalLayout_23.addLayout(self.horizontalLayout_4)
                self.horizontalSlider_age = QtWidgets.QSlider(self.frame_patient_settings)
                self.horizontalSlider_age.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSlider_age.setObjectName("horizontalSlider_age")
                self.verticalLayout_23.addWidget(self.horizontalSlider_age)
                self.horizontalLayout_6.addLayout(self.verticalLayout_23)
                self.line_2 = QtWidgets.QFrame(self.frame_patient_settings)
                self.line_2.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
                self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_2.setObjectName("line_2")
                self.horizontalLayout_6.addWidget(self.line_2)
                self.verticalLayout_3 = QtWidgets.QVBoxLayout()
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.label_age_2 = QtWidgets.QLabel(self.frame_patient_settings)
                self.label_age_2.setMinimumSize(QtCore.QSize(60, 0))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_age_2.setFont(font)
                self.label_age_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.label_age_2.setObjectName("label_age_2")
                self.horizontalLayout_2.addWidget(self.label_age_2)
                self.spinBox_volume_kg = QtWidgets.QSpinBox(self.frame_patient_settings)
                self.spinBox_volume_kg.setMinimumSize(QtCore.QSize(70, 35))
                font = QtGui.QFont()
                font.setPointSize(20)
                self.spinBox_volume_kg.setFont(font)
                self.spinBox_volume_kg.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                "QSpinBox::down-button { width: 32px; }")
                self.spinBox_volume_kg.setFrame(True)
                self.spinBox_volume_kg.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_volume_kg.setMinimum(4)
                self.spinBox_volume_kg.setMaximum(8)
                self.spinBox_volume_kg.setProperty("value", 6)
                self.spinBox_volume_kg.setObjectName("spinBox_volume_kg")
                self.horizontalLayout_2.addWidget(self.spinBox_volume_kg)
                self.verticalLayout_3.addLayout(self.horizontalLayout_2)
                self.horizontalSlider_age_2 = QtWidgets.QSlider(self.frame_patient_settings)
                self.horizontalSlider_age_2.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSlider_age_2.setObjectName("horizontalSlider_age_2")
                self.verticalLayout_3.addWidget(self.horizontalSlider_age_2)
                self.horizontalLayout_6.addLayout(self.verticalLayout_3)
                self.line_9 = QtWidgets.QFrame(self.frame_patient_settings)
                self.line_9.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
                self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_9.setObjectName("line_9")
                self.horizontalLayout_6.addWidget(self.line_9)
                self.verticalLayout = QtWidgets.QVBoxLayout()
                self.verticalLayout.setObjectName("verticalLayout")
                self.label_gender = QtWidgets.QLabel(self.frame_patient_settings)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_gender.setFont(font)
                self.label_gender.setAlignment(QtCore.Qt.AlignCenter)
                self.label_gender.setObjectName("label_gender")
                self.verticalLayout.addWidget(self.label_gender)
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.radioButton_female = QtWidgets.QRadioButton(self.frame_patient_settings)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.radioButton_female.setFont(font)
                self.radioButton_female.setObjectName("radioButton_female")
                self.horizontalLayout.addWidget(self.radioButton_female)
                self.radioButton_male = QtWidgets.QRadioButton(self.frame_patient_settings)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.radioButton_male.setFont(font)
                self.radioButton_male.setObjectName("radioButton_male")
                self.horizontalLayout.addWidget(self.radioButton_male)
                self.verticalLayout.addLayout(self.horizontalLayout)
                self.horizontalLayout_6.addLayout(self.verticalLayout)
                self.verticalLayout_4.addLayout(self.horizontalLayout_6)
                self.button_apply_age_hei_gen = QtWidgets.QPushButton(self.frame_patient_settings)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_apply_age_hei_gen.setFont(font)
                self.button_apply_age_hei_gen.setStyleSheet("background-color: rgb(169, 160, 157);")
                self.button_apply_age_hei_gen.setObjectName("button_apply_age_hei_gen")
                self.verticalLayout_4.addWidget(self.button_apply_age_hei_gen)
                self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
                self.gridLayout_2.addWidget(self.frame_patient_settings, 1, 0, 1, 1)
                patientSettingsWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(patientSettingsWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 22))
                self.menubar.setObjectName("menubar")
                patientSettingsWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(patientSettingsWindow)
                self.statusbar.setObjectName("statusbar")
                patientSettingsWindow.setStatusBar(self.statusbar)
                self.button_apply_age_hei_gen.clicked.connect(self.pressed_age_height_gender_button)
                self.horizontalSlider_height.setMinimum(20)
                self.horizontalSlider_height.setMaximum(220)
                self.horizontalSlider_height.setValue(self.spinBox_height.value())
                self.horizontalSlider_height.valueChanged.connect(self.update_height_slider)

                self.horizontalSlider_age.setMinimum(1)
                self.horizontalSlider_age.setMaximum(100)
                self.horizontalSlider_age.setValue(self.spinBox_age.value())
                self.horizontalSlider_age.valueChanged.connect(self.update_age_slider)

                self.horizontalSlider_age_2.setMinimum(4)
                self.horizontalSlider_age_2.setMaximum(8)
                self.horizontalSlider_age_2.setSingleStep(1)
                self.horizontalSlider_age_2.setValue(self.spinBox_volume_kg.value())
                self.horizontalSlider_age_2.valueChanged.connect(self.update_volume_kg_slider)

                self.retranslateUi(patientSettingsWindow)
                QtCore.QMetaObject.connectSlotsByName(patientSettingsWindow)

        def retranslateUi(self, patientSettingsWindow):
                """This method retranslateUi() sets the text and titles of the widgets."""
                _translate = QtCore.QCoreApplication.translate
                patientSettingsWindow.setWindowTitle(_translate("patientSettingsWindow", "Patient Settings"))
                self.label_5.setText(_translate("patientSettingsWindow", "Patient Settings"))
                self.label_height.setText(_translate("patientSettingsWindow", "HEIGHT \n"
                "(cm)"))
                self.label_age.setText(_translate("patientSettingsWindow", "AGE"))
                self.label_age_2.setText(_translate("patientSettingsWindow", "Volume per \n"
                " kg "))
                self.label_gender.setText(_translate("patientSettingsWindow", "GENDER"))
                self.radioButton_female.setText(_translate("patientSettingsWindow", "Female"))
                self.radioButton_male.setText(_translate("patientSettingsWindow", "Male"))
                self.button_apply_age_hei_gen.setText(_translate("patientSettingsWindow", "APPLY"))

        def pressed_age_height_gender_button(self):
                
                if self.radioButton_male.isChecked(): #In case male is selected
                        self.signals.res.emit(str(self.spinBox_height.value()) + "," + str(self.spinBox_age.value())+ "," + str(self.spinBox_volume_kg.value())
                        + "," + "Male")  # Return the values of each box as a string
                elif self.radioButton_female.isChecked():#In case female is selected
                        self.signals.res.emit(str(self.spinBox_height.value()) + "," + str(self.spinBox_age.value())+ "," + str(self.spinBox_volume_kg.value())
                        + "," + "Female")  # Return the values of each box as a string
                else: #In case no gender was selected, pop-up message
                        QtWidgets.QMessageBox.information(QtWidgets.QMainWindow(), "Attention!","You have to select a gender", QtWidgets.QMessageBox.Ok)
        def update_height_slider(self, event):
                self.spinBox_height.setValue(event)
        def update_age_slider(self, event):
                self.spinBox_age.setValue(event)
        def update_volume_kg_slider(self, event):
                self.spinBox_volume_kg.setValue(event)


class Ui_FlowCalculatorWindow(object):
        def setupUi(self, FlowCalculatorWindow):
                """
                Setup for GUI design for this class. We set the following properties:
                        - Grids/Frames/Layouts
                        - Widgets/Lines/Labels/input boxes/Buttons (properties as colour and sizes)
                        - Font properties
                """
                FlowCalculatorWindow.setObjectName("FlowCalculatorWindow")
                FlowCalculatorWindow.resize(554, 367)
                self.centralwidget = QtWidgets.QWidget(FlowCalculatorWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout.setObjectName("gridLayout")
                self.frame_flowcalculator = QtWidgets.QFrame(self.centralwidget)
                self.frame_flowcalculator.setMinimumSize(QtCore.QSize(500, 300))
                self.frame_flowcalculator.setMaximumSize(QtCore.QSize(1700, 600))
                self.frame_flowcalculator.setStyleSheet("background-color: rgb(164, 176, 179);")
                self.frame_flowcalculator.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_flowcalculator.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_flowcalculator.setObjectName("frame_flowcalculator")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_flowcalculator)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.verticalLayout_5 = QtWidgets.QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_14.setObjectName("horizontalLayout_14")
                spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_14.addItem(spacerItem)
                self.label_5 = QtWidgets.QLabel(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(30)
                self.label_5.setFont(font)
                self.label_5.setObjectName("label_5")
                self.horizontalLayout_14.addWidget(self.label_5)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.horizontalLayout_14.addItem(spacerItem1)
                self.verticalLayout_5.addLayout(self.horizontalLayout_14)
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                self.verticalLayout_4 = QtWidgets.QVBoxLayout()
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.verticalLayout_3 = QtWidgets.QVBoxLayout()
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.verticalLayout = QtWidgets.QVBoxLayout()
                self.verticalLayout.setObjectName("verticalLayout")
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.label_flow_rate = QtWidgets.QLabel(self.frame_flowcalculator)
                self.label_flow_rate.setMinimumSize(QtCore.QSize(120, 0))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_flow_rate.setFont(font)
                self.label_flow_rate.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.label_flow_rate.setObjectName("label_flow_rate")
                self.horizontalLayout.addWidget(self.label_flow_rate)
                self.spinBox_flow_rate = QtWidgets.QSpinBox(self.frame_flowcalculator)
                self.spinBox_flow_rate.setMinimumSize(QtCore.QSize(80, 35))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.spinBox_flow_rate.setFont(font)
                self.spinBox_flow_rate.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_flow_rate.setFrame(True)
                self.spinBox_flow_rate.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_flow_rate.setMinimum(0)
                self.spinBox_flow_rate.setMaximum(150)
                self.spinBox_flow_rate.setProperty("value", 25)
                self.spinBox_flow_rate.setObjectName("spinBox_flow_rate")
                self.horizontalLayout.addWidget(self.spinBox_flow_rate)
                self.verticalLayout.addLayout(self.horizontalLayout)
                self.horizontalSlider_flow_rate = QtWidgets.QSlider(self.frame_flowcalculator)
                self.horizontalSlider_flow_rate.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSlider_flow_rate.setObjectName("horizontalSlider_flow_rate")
                self.verticalLayout.addWidget(self.horizontalSlider_flow_rate)
                self.verticalLayout_3.addLayout(self.verticalLayout)
                self.verticalLayout_2 = QtWidgets.QVBoxLayout()
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.label_fio2 = QtWidgets.QLabel(self.frame_flowcalculator)
                self.label_fio2.setMinimumSize(QtCore.QSize(60, 0))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_fio2.setFont(font)
                self.label_fio2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.label_fio2.setObjectName("label_fio2")
                self.horizontalLayout_2.addWidget(self.label_fio2)
                self.spinBox_fio2 = QtWidgets.QSpinBox(self.frame_flowcalculator)
                self.spinBox_fio2.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(25)
                self.spinBox_fio2.setFont(font)
                self.spinBox_fio2.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_fio2.setFrame(True)
                self.spinBox_fio2.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_fio2.setMaximum(100)
                self.spinBox_fio2.setProperty("value", 21)
                self.spinBox_fio2.setObjectName("spinBox_fio2")
                self.horizontalLayout_2.addWidget(self.spinBox_fio2)
                self.verticalLayout_2.addLayout(self.horizontalLayout_2)
                self.horizontalSlider_fio2 = QtWidgets.QSlider(self.frame_flowcalculator)
                self.horizontalSlider_fio2.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSlider_fio2.setObjectName("horizontalSlider_fio2")
                self.verticalLayout_2.addWidget(self.horizontalSlider_fio2)
                self.verticalLayout_3.addLayout(self.verticalLayout_2)
                self.verticalLayout_4.addLayout(self.verticalLayout_3)
                self.button_calculate_flow_rate = QtWidgets.QPushButton(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_calculate_flow_rate.setFont(font)
                self.button_calculate_flow_rate.setStyleSheet("background-color: rgb(169, 160, 157);")
                self.button_calculate_flow_rate.setObjectName("button_calculate_flow_rate")
                self.verticalLayout_4.addWidget(self.button_calculate_flow_rate)
                self.horizontalLayout_3.addLayout(self.verticalLayout_4)
                self.line_10 = QtWidgets.QFrame(self.frame_flowcalculator)
                self.line_10.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
                self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_10.setObjectName("line_10")
                self.horizontalLayout_3.addWidget(self.line_10)
                self.verticalLayout_31 = QtWidgets.QVBoxLayout()
                self.verticalLayout_31.setObjectName("verticalLayout_31")
                self.verticalLayout_30 = QtWidgets.QVBoxLayout()
                self.verticalLayout_30.setObjectName("verticalLayout_30")
                spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_30.addItem(spacerItem2)
                self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_11.setObjectName("horizontalLayout_11")
                self.label_air_flow_rate = QtWidgets.QLabel(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_air_flow_rate.setFont(font)
                self.label_air_flow_rate.setObjectName("label_air_flow_rate")
                self.horizontalLayout_11.addWidget(self.label_air_flow_rate)
                self.label_air_flow_res = QtWidgets.QLabel(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_air_flow_res.setFont(font)
                self.label_air_flow_res.setObjectName("label_air_flow_res")
                self.horizontalLayout_11.addWidget(self.label_air_flow_res)
                self.verticalLayout_30.addLayout(self.horizontalLayout_11)
                self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_9.setObjectName("horizontalLayout_9")
                self.label_oxygen_flow_rate = QtWidgets.QLabel(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_oxygen_flow_rate.setFont(font)
                self.label_oxygen_flow_rate.setObjectName("label_oxygen_flow_rate")
                self.horizontalLayout_9.addWidget(self.label_oxygen_flow_rate)
                self.label_oxygen_flow_res = QtWidgets.QLabel(self.frame_flowcalculator)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_oxygen_flow_res.setFont(font)
                self.label_oxygen_flow_res.setObjectName("label_oxygen_flow_res")
                self.horizontalLayout_9.addWidget(self.label_oxygen_flow_res)
                self.verticalLayout_30.addLayout(self.horizontalLayout_9)
                self.verticalLayout_31.addLayout(self.verticalLayout_30)
                spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_31.addItem(spacerItem3)
                self.horizontalLayout_3.addLayout(self.verticalLayout_31)
                self.verticalLayout_5.addLayout(self.horizontalLayout_3)
                self.gridLayout_2.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
                self.gridLayout.addWidget(self.frame_flowcalculator, 0, 0, 1, 1)
                FlowCalculatorWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(FlowCalculatorWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 554, 22))
                self.menubar.setObjectName("menubar")
                FlowCalculatorWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(FlowCalculatorWindow)
                self.statusbar.setObjectName("statusbar")
                FlowCalculatorWindow.setStatusBar(self.statusbar)
                self.button_calculate_flow_rate.clicked.connect(self.calculate_flow)


                self.horizontalSlider_flow_rate.setMinimum(0)
                self.horizontalSlider_flow_rate.setMaximum(150)
                self.horizontalSlider_flow_rate.setSingleStep(1)
                self.horizontalSlider_flow_rate.setValue(self.spinBox_flow_rate.value())
                self.horizontalSlider_flow_rate.valueChanged.connect(self.update_flow_rate)

                self.horizontalSlider_fio2.setMinimum(0)
                self.horizontalSlider_fio2.setMaximum(100)
                self.horizontalSlider_fio2.setSingleStep(1)
                self.horizontalSlider_fio2.setValue(self.spinBox_fio2.value())
                self.horizontalSlider_fio2.valueChanged.connect(self.update_fio2)

                self.retranslateUi_flow_calculation(FlowCalculatorWindow)
                QtCore.QMetaObject.connectSlotsByName(FlowCalculatorWindow)

        def retranslateUi_flow_calculation(self, FlowCalculatorWindow):
                """
                This method retranslateUi() sets the text and titles of the widgets.
                """
                _translate = QtCore.QCoreApplication.translate
                FlowCalculatorWindow.setWindowTitle(_translate("FlowCalculatorWindow", "MainWindow"))
                self.label_5.setText(_translate("FlowCalculatorWindow", "Flow calculator"))
                self.label_flow_rate.setText(_translate("FlowCalculatorWindow", "Flow rate"))
                self.label_fio2.setText(_translate("FlowCalculatorWindow", "<html><head/><body><p>FiO<span style=\" vertical-align:sub;\">2 </span>(%)</p></body></html>"))
                self.button_calculate_flow_rate.setText(_translate("FlowCalculatorWindow", "CALCULATE"))
                self.label_air_flow_rate.setText(_translate("FlowCalculatorWindow", "Air Flow Rate:"))
                self.label_air_flow_res.setText(_translate("FlowCalculatorWindow", "0"))
                self.label_oxygen_flow_rate.setText(_translate("FlowCalculatorWindow", "<html><head/><body><p>O<span style=\" vertical-align:sub;\">2</span> Flow Rate :</p></body></html>"))
                self.label_oxygen_flow_res.setText(_translate("FlowCalculatorWindow", "0"))
        def calculate_flow(self):
                total_air_flow = round((self.spinBox_flow_rate.value()*(self.spinBox_fio2.value()-21))/79,1)
                total_oxygen_flow = self.spinBox_flow_rate.value() - 0
                self.label_air_flow_res.setText(str(total_air_flow))
                self.label_oxygen_flow_res.setText(str(total_oxygen_flow))
                
        def update_flow_rate(self, event):
                self.spinBox_flow_rate.setValue(event)
        def update_fio2(self, event):
                self.spinBox_fio2.setValue(event)

class Ui_MainWindow(object):
        def __init__(self):
                super(Ui_MainWindow, self).__init__()

        def openFlowCalculator(self):
                """
                Method in charge of implementing the Flow Calculator window. It is called when the button "button_flowcalculator" is clicked.
                """
                self.flow_calculator_window = QtWidgets.QMainWindow()
                self.ui_flow_calculator = Ui_FlowCalculatorWindow()
                self.ui_flow_calculator.setupUi(self.flow_calculator_window)
                self.flow_calculator_window.show()

        def openpatientSettings(self):
                """
                Method in charge of implementing the Patient Settings window. It is called when the button "button_patient_settings" is clicked.
                """
                self.patient_settings_window = QtWidgets.QMainWindow()
                self.ui_patient_settings = Ui_patientSettingsWindow()
                self.ui_patient_settings.setupUi(self.patient_settings_window)
                self.patient_settings_window.show()
                self.ui_patient_settings.signals.res.connect(self.read_patient_settings) #Obtain the values set by the user and send them to read_patient_settings() funtion

        def setupUi(self, MainWindow):
                """
                Setup for GUI design for this class. We set the following properties:
                        - Grids/Frames/Layouts
                        - Widgets/Lines/Labels/input boxes/Buttons (properties as colour and sizes)
                        - Font properties
                """
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(956, 800)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.frame_top_left_labels = QtWidgets.QFrame(self.centralwidget)
                self.frame_top_left_labels.setMinimumSize(QtCore.QSize(155, 450))
                self.frame_top_left_labels.setMaximumSize(QtCore.QSize(190, 700))
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
                self.frame_top_left_labels.setPalette(palette)
                font = QtGui.QFont()
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.frame_top_left_labels.setFont(font)
                self.frame_top_left_labels.setStyleSheet("background-color: rgb(177, 202, 136);")
                self.frame_top_left_labels.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_top_left_labels.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_top_left_labels.setObjectName("frame_top_left_labels")
                self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_top_left_labels)
                self.verticalLayout_7.setObjectName("verticalLayout_7")
                self.verticalLayout = QtWidgets.QVBoxLayout()
                self.verticalLayout.setObjectName("verticalLayout")
                self.label_frequency = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_frequency.setFont(font)
                self.label_frequency.setAlignment(QtCore.Qt.AlignCenter)
                self.label_frequency.setObjectName("label_frequency")
                self.verticalLayout.addWidget(self.label_frequency)
                self.label_frequency_value = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_frequency_value.setFont(font)
                self.label_frequency_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_frequency_value.setObjectName("label_frequency_value")
                self.verticalLayout.addWidget(self.label_frequency_value)
                self.label_frequency_unit = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_frequency_unit.setFont(font)
                self.label_frequency_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_frequency_unit.setObjectName("label_frequency_unit")
                self.verticalLayout.addWidget(self.label_frequency_unit)
                self.verticalLayout_7.addLayout(self.verticalLayout)
                self.line_2 = QtWidgets.QFrame(self.frame_top_left_labels)
                self.line_2.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_2.setObjectName("line_2")
                self.verticalLayout_7.addWidget(self.line_2)
                self.verticalLayout_3 = QtWidgets.QVBoxLayout()
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.label_tidal_vol = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_tidal_vol.setFont(font)
                self.label_tidal_vol.setAlignment(QtCore.Qt.AlignCenter)
                self.label_tidal_vol.setObjectName("label_tidal_vol")
                self.verticalLayout_3.addWidget(self.label_tidal_vol)
                self.label_tidal_vol_value = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_tidal_vol_value.setFont(font)
                self.label_tidal_vol_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_tidal_vol_value.setObjectName("label_tidal_vol_value")
                self.verticalLayout_3.addWidget(self.label_tidal_vol_value)
                self.label_tidal_vol_unit = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_tidal_vol_unit.setFont(font)
                self.label_tidal_vol_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_tidal_vol_unit.setObjectName("label_tidal_vol_unit")
                self.verticalLayout_3.addWidget(self.label_tidal_vol_unit)
                self.verticalLayout_7.addLayout(self.verticalLayout_3)
                self.line_3 = QtWidgets.QFrame(self.frame_top_left_labels)
                self.line_3.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_3.setObjectName("line_3")
                self.verticalLayout_7.addWidget(self.line_3)
                self.verticalLayout_4 = QtWidgets.QVBoxLayout()
                self.verticalLayout_4.setObjectName("verticalLayout_4")
                self.label_min_vent = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_min_vent.setFont(font)
                self.label_min_vent.setAlignment(QtCore.Qt.AlignCenter)
                self.label_min_vent.setObjectName("label_min_vent")
                self.verticalLayout_4.addWidget(self.label_min_vent)
                self.label_min_vent_value = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_min_vent_value.setFont(font)
                self.label_min_vent_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_min_vent_value.setObjectName("label_min_vent_value")
                self.verticalLayout_4.addWidget(self.label_min_vent_value)
                self.label_min_vent_unit = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_min_vent_unit.setFont(font)
                self.label_min_vent_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_min_vent_unit.setObjectName("label_min_vent_unit")
                self.verticalLayout_4.addWidget(self.label_min_vent_unit)
                self.verticalLayout_7.addLayout(self.verticalLayout_4)
                self.line_4 = QtWidgets.QFrame(self.frame_top_left_labels)
                self.line_4.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_4.setObjectName("line_4")
                self.verticalLayout_7.addWidget(self.line_4)
                self.verticalLayout_5 = QtWidgets.QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                self.label_resistance = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_resistance.setFont(font)
                self.label_resistance.setAlignment(QtCore.Qt.AlignCenter)
                self.label_resistance.setObjectName("label_resistance")
                self.verticalLayout_5.addWidget(self.label_resistance)
                self.label_resistance_value = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_resistance_value.setFont(font)
                self.label_resistance_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_resistance_value.setObjectName("label_resistance_value")
                self.verticalLayout_5.addWidget(self.label_resistance_value)
                self.label_resistance_unit = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_resistance_unit.setFont(font)
                self.label_resistance_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_resistance_unit.setObjectName("label_resistance_unit")
                self.verticalLayout_5.addWidget(self.label_resistance_unit)
                self.verticalLayout_7.addLayout(self.verticalLayout_5)
                self.line_5 = QtWidgets.QFrame(self.frame_top_left_labels)
                self.line_5.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_5.setObjectName("line_5")
                self.verticalLayout_7.addWidget(self.line_5)
                self.verticalLayout_6 = QtWidgets.QVBoxLayout()
                self.verticalLayout_6.setObjectName("verticalLayout_6")
                self.label_complains = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_complains.setFont(font)
                self.label_complains.setAlignment(QtCore.Qt.AlignCenter)
                self.label_complains.setObjectName("label_complains")
                self.verticalLayout_6.addWidget(self.label_complains)
                self.label_complains_value = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_complains_value.setFont(font)
                self.label_complains_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_complains_value.setObjectName("label_complains_value")
                self.verticalLayout_6.addWidget(self.label_complains_value)
                self.label_complains_unit = QtWidgets.QLabel(self.frame_top_left_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_complains_unit.setFont(font)
                self.label_complains_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_complains_unit.setObjectName("label_complains_unit")
                self.verticalLayout_6.addWidget(self.label_complains_unit)
                self.verticalLayout_7.addLayout(self.verticalLayout_6)
                self.gridLayout_3.addWidget(self.frame_top_left_labels, 0, 0, 1, 1)
                self.frame_plots = QtWidgets.QFrame(self.centralwidget)
                self.frame_plots.setMinimumSize(QtCore.QSize(0, 400))
                self.frame_plots.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_plots.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_plots.setObjectName("frame_plots")
                self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_plots)
                self.gridLayout_4.setObjectName("gridLayout_4")
                self.label_x_axis = QtWidgets.QLabel(self.frame_plots)
                font = QtGui.QFont()
                font.setPointSize(17)
                self.label_x_axis.setFont(font)
                labelStyle = {'color': '#FFF', 'font-size': '17pt'}
                pg.setConfigOption('foreground', 'w')
                self.label_x_axis.setAlignment(QtCore.Qt.AlignCenter)
                self.label_x_axis.setObjectName("label_x_axis")
                self.gridLayout_4.addWidget(self.label_x_axis, 3, 0, 1, 1)
                self.graphicsView_pressure = pg.PlotWidget(self.frame_plots)
                self.graphicsView_pressure.setMinimumSize(QtCore.QSize(0, 100))
                self.graphicsView_pressure.setObjectName("graphicsView_pressure")
                self.graphicsView_pressure.setLabel('left', "<html><body><p>P (cm H<span style=\" vertical-align:sub;\">2</span>O)</p></body></html>", **labelStyle)
                # self.graphicsView_pressure.setConfigOption('foreground ', 'r')
                
                self.gridLayout_4.addWidget(self.graphicsView_pressure, 0, 0, 1, 1)
                self.graphicsView_volume = pg.PlotWidget(self.frame_plots)
                self.graphicsView_volume.setMinimumSize(QtCore.QSize(0, 100))
                self.graphicsView_volume.setObjectName("graphicsView_volume")
                self.graphicsView_volume.setLabel('left', 'Volume (mL)', **labelStyle)
                # self.graphicsView_volume.setConfigOption('foreground',  'y')

                self.gridLayout_4.addWidget(self.graphicsView_volume, 1, 0, 1, 1)
                self.graphicsView_flow = pg.PlotWidget(self.frame_plots)
                self.graphicsView_flow.setMinimumSize(QtCore.QSize(0, 100))
                self.graphicsView_flow.setObjectName("graphicsView_flow")
                self.graphicsView_flow.setLabel('left', 'Flow (lpm)', **labelStyle)
                self.gridLayout_4.addWidget(self.graphicsView_flow, 2, 0, 1, 1)
                # self.graphicsView_flow.setConfigOption('foreground', ' g')

                self.gridLayout_3.addWidget(self.frame_plots, 0, 1, 1, 1)
                self.frame_3 = QtWidgets.QFrame(self.centralwidget)
                self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
                self.frame_3.setMaximumSize(QtCore.QSize(1700, 600))
                self.frame_3.setStyleSheet("background-color: rgb(164, 176, 179);")
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.gridLayout = QtWidgets.QGridLayout(self.frame_3)
                self.gridLayout.setObjectName("gridLayout")
                self.verticalLayout_22 = QtWidgets.QVBoxLayout()
                self.verticalLayout_22.setObjectName("verticalLayout_22")
                self.button_patient_settings = QtWidgets.QPushButton(self.frame_3)
                font = QtGui.QFont()
                font.setPointSize(18)
                self.button_patient_settings.setFont(font)
                self.button_patient_settings.setStyleSheet("QPushButton {\n"
                                                        "    color: #333;\n"
                                                        "    border: 2px solid #555;\n"
                                                        "    border-radius: 20px;\n"
                                                        "    border-style: outset;\n"
                                                        "    padding: 5px;\n"
                                                        "    background-color: rgb(169, 160, 157);\n"
                                                        "\n"
                                                        "    }\n"
                                                        "QPushButton:pressed {\n"
                                                        "    border-style: inset;\n"
                                                        "\n"
                                                        "    }\n"
                                                        "")
                self.button_patient_settings.setObjectName("button_patient_settings")
                self.verticalLayout_22.addWidget(self.button_patient_settings)
                self.button_flowcalculator = QtWidgets.QPushButton(self.frame_3)
                font = QtGui.QFont()
                font.setPointSize(18)
                self.button_flowcalculator.setFont(font)
                self.button_flowcalculator.setStyleSheet("QPushButton {\n"
                                                        "    color: #333;\n"
                                                        "    border: 2px solid #555;\n"
                                                        "    border-radius: 20px;\n"
                                                        "    border-style: outset;\n"
                                                        "    padding: 5px;\n"
                                                        "    background-color: rgb(169, 160, 157);\n"
                                                        "\n"
                                                        "    }\n"
                                                        "QPushButton:pressed {\n"
                                                        "    border-style: inset;\n"
                                                        "\n"
                                                        "    }\n"
                                                        "")
                self.button_flowcalculator.setObjectName("button_flowcalculator")
                self.verticalLayout_22.addWidget(self.button_flowcalculator)
                self.button_alarm = QtWidgets.QPushButton(self.frame_3)
                self.button_alarm.setMinimumSize(QtCore.QSize(0, 60))
                font = QtGui.QFont()
                font.setPointSize(30)
                font.setBold(True)
                font.setWeight(75)
                self.button_alarm.setFont(font)
                self.button_alarm.setStyleSheet("\n"
                                                "QPushButton {\n"
                                                "    color: #333;\n"
                                                "    border: 2px solid #555;\n"
                                                "    border-radius: 20px;\n"
                                                "    border-style: outset;\n"
                                                "    padding: 5px;\n"
                                                "    background-color: rgb(220, 92, 24);\n"
                                                "image:url(./images/bell.png);\n"
                                                "\n"
                                                "    }\n"
                                                "QPushButton:pressed {\n"
                                                "    border-style: inset;\n"
                                                "\n"
                                                "    }\n"
                                                "\n"
                                                "")
                self.button_alarm.setText("")
                icon = QtGui.QIcon.fromTheme("Bell")
                self.button_alarm.setIcon(icon)
                self.button_alarm.setObjectName("button_alarm")
                self.verticalLayout_22.addWidget(self.button_alarm)
                self.gridLayout.addLayout(self.verticalLayout_22, 0, 0, 1, 1)
                self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)
                self.tab_widget_modes = QtWidgets.QTabWidget(self.centralwidget)
                self.tab_widget_modes.setEnabled(True)
                self.tab_widget_modes.setMinimumSize(QtCore.QSize(0, 220))
                self.tab_widget_modes.setMaximumSize(QtCore.QSize(16777215, 500))
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(15)
                self.tab_widget_modes.setFont(font)
                self.tab_widget_modes.setStyleSheet("")
                self.tab_widget_modes.setTabPosition(QtWidgets.QTabWidget.North)
                self.tab_widget_modes.setTabShape(QtWidgets.QTabWidget.Rounded)
                self.tab_widget_modes.setIconSize(QtCore.QSize(16, 16))
                self.tab_widget_modes.setUsesScrollButtons(True)
                self.tab_widget_modes.setTabsClosable(False)
                self.tab_widget_modes.setMovable(False)
                self.tab_widget_modes.setTabBarAutoHide(False)
                self.tab_widget_modes.setObjectName("tab_widget_modes")
                self.volume_assist_tab = QtWidgets.QWidget()
                self.volume_assist_tab.setObjectName("volume_assist_tab")
                self.gridLayout_6 = QtWidgets.QGridLayout(self.volume_assist_tab)
                self.gridLayout_6.setObjectName("gridLayout_6")
                self.verticalLayout_25 = QtWidgets.QVBoxLayout()
                self.verticalLayout_25.setObjectName("verticalLayout_25")
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                self.verticalLayout_14 = QtWidgets.QVBoxLayout()
                self.verticalLayout_14.setObjectName("verticalLayout_14")
                self.label_cont_mand_vent_frequency = QtWidgets.QLabel(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_cont_mand_vent_frequency.setFont(font)
                self.label_cont_mand_vent_frequency.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cont_mand_vent_frequency.setObjectName("label_cont_mand_vent_frequency")
                self.verticalLayout_14.addWidget(self.label_cont_mand_vent_frequency)
                self.spinBox_cont_mand_vent_freq_value = QtWidgets.QSpinBox(self.volume_assist_tab)
                self.spinBox_cont_mand_vent_freq_value.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_cont_mand_vent_freq_value.setFont(font)
                self.spinBox_cont_mand_vent_freq_value.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_cont_mand_vent_freq_value.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_cont_mand_vent_freq_value.setMinimum(10)
                self.spinBox_cont_mand_vent_freq_value.setMaximum(30)
                self.spinBox_cont_mand_vent_freq_value.setSingleStep(2)
                self.spinBox_cont_mand_vent_freq_value.setObjectName("spinBox_cont_mand_vent_freq_value")
                self.verticalLayout_14.addWidget(self.spinBox_cont_mand_vent_freq_value)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_14.addItem(spacerItem)
                self.horizontalLayout_3.addLayout(self.verticalLayout_14)
                self.verticalLayout_18 = QtWidgets.QVBoxLayout()
                self.verticalLayout_18.setObjectName("verticalLayout_18")
                self.label_cont_mand_vent_tid_vol = QtWidgets.QLabel(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_cont_mand_vent_tid_vol.setFont(font)
                self.label_cont_mand_vent_tid_vol.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cont_mand_vent_tid_vol.setObjectName("label_cont_mand_vent_tid_vol")
                self.verticalLayout_18.addWidget(self.label_cont_mand_vent_tid_vol)
                self.spinBox_cont_mand_vent_tid_vol_value = QtWidgets.QSpinBox(self.volume_assist_tab)
                self.spinBox_cont_mand_vent_tid_vol_value.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_cont_mand_vent_tid_vol_value.setFont(font)
                self.spinBox_cont_mand_vent_tid_vol_value.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_cont_mand_vent_tid_vol_value.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_cont_mand_vent_tid_vol_value.setMinimum(200)
                self.spinBox_cont_mand_vent_tid_vol_value.setMaximum(800)
                self.spinBox_cont_mand_vent_tid_vol_value.setSingleStep(50)
                self.spinBox_cont_mand_vent_tid_vol_value.setProperty("value", 250)
                self.spinBox_cont_mand_vent_tid_vol_value.setObjectName("spinBox_cont_mand_vent_tid_vol_value")
                self.verticalLayout_18.addWidget(self.spinBox_cont_mand_vent_tid_vol_value)
                spacerItem1 = QtWidgets.QSpacerItem(142, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_18.addItem(spacerItem1)
                self.horizontalLayout_3.addLayout(self.verticalLayout_18)
                self.verticalLayout_19 = QtWidgets.QVBoxLayout()
                self.verticalLayout_19.setObjectName("verticalLayout_19")
                self.label_cont_mand_vent_insp_pause = QtWidgets.QLabel(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_cont_mand_vent_insp_pause.setFont(font)
                self.label_cont_mand_vent_insp_pause.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cont_mand_vent_insp_pause.setObjectName("label_cont_mand_vent_insp_pause")
                self.verticalLayout_19.addWidget(self.label_cont_mand_vent_insp_pause)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value = QtWidgets.QDoubleSpinBox(self.volume_assist_tab)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setFont(font)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setStyleSheet("QDoubleSpinBox::up-button { width: 32px; }\n"
                        "QDoubleSpinBox::down-button { width: 32px; }")
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setAlignment(QtCore.Qt.AlignCenter)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setDecimals(1)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setMaximum(0.5)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setSingleStep(0.1)
                self.doubleSpinBox_cont_mand_vent_insp_pause_value.setObjectName("doubleSpinBox_cont_mand_vent_insp_pause_value")
                self.verticalLayout_19.addWidget(self.doubleSpinBox_cont_mand_vent_insp_pause_value)
                spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_19.addItem(spacerItem2)
                self.horizontalLayout_3.addLayout(self.verticalLayout_19)
                self.verticalLayout_20 = QtWidgets.QVBoxLayout()
                self.verticalLayout_20.setObjectName("verticalLayout_20")
                self.label_cont_mand_vent_I_E = QtWidgets.QLabel(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_cont_mand_vent_I_E.setFont(font)
                self.label_cont_mand_vent_I_E.setStyleSheet("")
                self.label_cont_mand_vent_I_E.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cont_mand_vent_I_E.setObjectName("label_cont_mand_vent_I_E")
                self.verticalLayout_20.addWidget(self.label_cont_mand_vent_I_E)
                self.spinBox_cont_mand_vent_I_E_value = QtWidgets.QSpinBox(self.volume_assist_tab)
                self.spinBox_cont_mand_vent_I_E_value.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_cont_mand_vent_I_E_value.setFont(font)
                self.spinBox_cont_mand_vent_I_E_value.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_cont_mand_vent_I_E_value.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_cont_mand_vent_I_E_value.setMinimum(1)
                self.spinBox_cont_mand_vent_I_E_value.setMaximum(3)
                self.spinBox_cont_mand_vent_I_E_value.setProperty("value", 1)
                self.spinBox_cont_mand_vent_I_E_value.setObjectName("spinBox_cont_mand_vent_I_E_value")
                self.verticalLayout_20.addWidget(self.spinBox_cont_mand_vent_I_E_value)
                spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_20.addItem(spacerItem3)
                self.horizontalLayout_3.addLayout(self.verticalLayout_20)
                self.verticalLayout_21 = QtWidgets.QVBoxLayout()
                self.verticalLayout_21.setObjectName("verticalLayout_21")
                self.label_cont_mand_vent_PIP = QtWidgets.QLabel(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_cont_mand_vent_PIP.setFont(font)
                self.label_cont_mand_vent_PIP.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cont_mand_vent_PIP.setObjectName("label_cont_mand_vent_PIP")
                self.verticalLayout_21.addWidget(self.label_cont_mand_vent_PIP)
                self.spinBox_cont_mand_vent_PIP_value = QtWidgets.QSpinBox(self.volume_assist_tab)
                self.spinBox_cont_mand_vent_PIP_value.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_cont_mand_vent_PIP_value.setFont(font)
                self.spinBox_cont_mand_vent_PIP_value.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_cont_mand_vent_PIP_value.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_cont_mand_vent_PIP_value.setMinimum(10)
                self.spinBox_cont_mand_vent_PIP_value.setMaximum(30)
                self.spinBox_cont_mand_vent_PIP_value.setProperty("value", 20)
                self.spinBox_cont_mand_vent_PIP_value.setObjectName("spinBox_cont_mand_vent_PIP_value")
                self.verticalLayout_21.addWidget(self.spinBox_cont_mand_vent_PIP_value)
                spacerItem4 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_21.addItem(spacerItem4)
                self.horizontalLayout_3.addLayout(self.verticalLayout_21)
                self.verticalLayout_25.addLayout(self.horizontalLayout_3)
                self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_5.setObjectName("horizontalLayout_5")
                self.button_cont_mand_asist_start = QtWidgets.QPushButton(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_cont_mand_asist_start.setFont(font)
                self.button_cont_mand_asist_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.button_cont_mand_asist_start.setStyleSheet("background-color: rgb(169, 160, 157);")
                self.button_cont_mand_asist_start.setObjectName("button_cont_mand_asist_start")
                self.horizontalLayout_5.addWidget(self.button_cont_mand_asist_start)
                self.button_cont_mand_asist_update = QtWidgets.QPushButton(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_cont_mand_asist_update.setFont(font)
                self.button_cont_mand_asist_update.setStyleSheet("background-color: rgb(255, 160, 80);")
                self.button_cont_mand_asist_update.setObjectName("button_cont_mand_asist_update")
                self.button_cont_mand_asist_update.setEnabled(False)
                self.horizontalLayout_5.addWidget(self.button_cont_mand_asist_update)
                self.button_cont_mand_asist_stop = QtWidgets.QPushButton(self.volume_assist_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_cont_mand_asist_stop.setFont(font)
                self.button_cont_mand_asist_stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.button_cont_mand_asist_stop.setStyleSheet("background-color: rgb(222, 0, 0);")
                self.button_cont_mand_asist_stop.setObjectName("button_cont_mand_asist_stop")
                self.horizontalLayout_5.addWidget(self.button_cont_mand_asist_stop)
                self.verticalLayout_25.addLayout(self.horizontalLayout_5)
                self.gridLayout_6.addLayout(self.verticalLayout_25, 0, 0, 1, 1)
                self.tab_widget_modes.addTab(self.volume_assist_tab, "")
                self.pressure_assit_tab = QtWidgets.QWidget()
                self.pressure_assit_tab.setObjectName("pressure_assit_tab")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.pressure_assit_tab)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.verticalLayout_23 = QtWidgets.QVBoxLayout()
                self.verticalLayout_23.setObjectName("verticalLayout_23")
                self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_4.setObjectName("horizontalLayout_4")
                self.verticalLayout_8 = QtWidgets.QVBoxLayout()
                self.verticalLayout_8.setObjectName("verticalLayout_8")
                self.label_asis_cont_frequency = QtWidgets.QLabel(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_asis_cont_frequency.setFont(font)
                self.label_asis_cont_frequency.setAlignment(QtCore.Qt.AlignCenter)
                self.label_asis_cont_frequency.setObjectName("label_asis_cont_frequency")
                self.verticalLayout_8.addWidget(self.label_asis_cont_frequency)
                self.spinBox_asis_cont_frequency = QtWidgets.QSpinBox(self.pressure_assit_tab)
                self.spinBox_asis_cont_frequency.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_asis_cont_frequency.setFont(font)
                self.spinBox_asis_cont_frequency.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_asis_cont_frequency.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_asis_cont_frequency.setMinimum(10)
                self.spinBox_asis_cont_frequency.setMaximum(30)
                self.spinBox_asis_cont_frequency.setSingleStep(2)
                self.spinBox_asis_cont_frequency.setProperty("value", 20)
                self.spinBox_asis_cont_frequency.setObjectName("spinBox_asis_cont_frequency")
                self.verticalLayout_8.addWidget(self.spinBox_asis_cont_frequency)
                spacerItem5 = QtWidgets.QSpacerItem(142, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_8.addItem(spacerItem5)
                self.horizontalLayout_4.addLayout(self.verticalLayout_8)
                self.verticalLayout_17 = QtWidgets.QVBoxLayout()
                self.verticalLayout_17.setObjectName("verticalLayout_17")
                self.label_asis_cont_tid_vol = QtWidgets.QLabel(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_asis_cont_tid_vol.setFont(font)
                self.label_asis_cont_tid_vol.setAlignment(QtCore.Qt.AlignCenter)
                self.label_asis_cont_tid_vol.setObjectName("label_asis_cont_tid_vol")
                self.verticalLayout_17.addWidget(self.label_asis_cont_tid_vol)
                self.spinBox_asis_cont_tid_vol = QtWidgets.QSpinBox(self.pressure_assit_tab)
                self.spinBox_asis_cont_tid_vol.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_asis_cont_tid_vol.setFont(font)
                self.spinBox_asis_cont_tid_vol.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_asis_cont_tid_vol.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_asis_cont_tid_vol.setMinimum(200)
                self.spinBox_asis_cont_tid_vol.setMaximum(800)
                self.spinBox_asis_cont_tid_vol.setSingleStep(50)
                self.spinBox_asis_cont_tid_vol.setProperty("value", 250)
                self.spinBox_asis_cont_tid_vol.setObjectName("spinBox_asis_cont_tid_vol")
                self.verticalLayout_17.addWidget(self.spinBox_asis_cont_tid_vol)
                spacerItem6 = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_17.addItem(spacerItem6)
                self.horizontalLayout_4.addLayout(self.verticalLayout_17)
                self.verticalLayout_16 = QtWidgets.QVBoxLayout()
                self.verticalLayout_16.setObjectName("verticalLayout_16")
                self.label_asis_cont_insp_pause = QtWidgets.QLabel(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_asis_cont_insp_pause.setFont(font)
                self.label_asis_cont_insp_pause.setStyleSheet("")
                self.label_asis_cont_insp_pause.setAlignment(QtCore.Qt.AlignCenter)
                self.label_asis_cont_insp_pause.setObjectName("label_asis_cont_insp_pause")
                self.verticalLayout_16.addWidget(self.label_asis_cont_insp_pause)
                self.doubleSpinBox_insp_pause = QtWidgets.QDoubleSpinBox(self.pressure_assit_tab)
                self.doubleSpinBox_insp_pause.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.doubleSpinBox_insp_pause.setFont(font)
                self.doubleSpinBox_insp_pause.setToolTipDuration(-1)
                self.doubleSpinBox_insp_pause.setStyleSheet("QDoubleSpinBox::up-button { width: 32px; }\n"
                        "QDoubleSpinBox::down-button { width: 32px; }")
                self.doubleSpinBox_insp_pause.setAlignment(QtCore.Qt.AlignCenter)
                self.doubleSpinBox_insp_pause.setDecimals(1)
                self.doubleSpinBox_insp_pause.setMaximum(0.5)
                self.doubleSpinBox_insp_pause.setSingleStep(0.1)
                self.doubleSpinBox_insp_pause.setProperty("value", 0.2)
                self.doubleSpinBox_insp_pause.setObjectName("doubleSpinBox_insp_pause")
                self.verticalLayout_16.addWidget(self.doubleSpinBox_insp_pause)
                spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_16.addItem(spacerItem7)
                self.horizontalLayout_4.addLayout(self.verticalLayout_16)
                self.verticalLayout_12 = QtWidgets.QVBoxLayout()
                self.verticalLayout_12.setObjectName("verticalLayout_12")
                self.label_asis_cont_trigger = QtWidgets.QLabel(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_asis_cont_trigger.setFont(font)
                self.label_asis_cont_trigger.setAlignment(QtCore.Qt.AlignCenter)
                self.label_asis_cont_trigger.setObjectName("label_asis_cont_trigger")
                self.verticalLayout_12.addWidget(self.label_asis_cont_trigger)
                self.spinBox_asis_cont_trigger_pre_flow = QtWidgets.QDoubleSpinBox(self.pressure_assit_tab)
                self.spinBox_asis_cont_trigger_pre_flow.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_asis_cont_trigger_pre_flow.setFont(font)
                self.spinBox_asis_cont_trigger_pre_flow.setStyleSheet("QDoubleSpinBox::up-button { width: 32px; }\n"
                        "QDoubleSpinBox::down-button { width: 32px; }")
                self.spinBox_asis_cont_trigger_pre_flow.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_asis_cont_trigger_pre_flow.setMinimum(-5.0)
                self.spinBox_asis_cont_trigger_pre_flow.setObjectName("spinBox_asis_cont_trigger_pre_flow")
                self.verticalLayout_12.addWidget(self.spinBox_asis_cont_trigger_pre_flow)
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.radioButton_pressure = QtWidgets.QRadioButton(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(17)
                self.radioButton_pressure.setFont(font)
                self.radioButton_pressure.setObjectName("radioButton_pressure")
                self.horizontalLayout_2.addWidget(self.radioButton_pressure)
                self.radioButton_flow = QtWidgets.QRadioButton(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(17)
                self.radioButton_flow.setFont(font)
                self.radioButton_flow.setObjectName("radioButton_flow")
                self.horizontalLayout_2.addWidget(self.radioButton_flow)
                self.verticalLayout_12.addLayout(self.horizontalLayout_2)
                spacerItem8 = QtWidgets.QSpacerItem(156, 146, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_12.addItem(spacerItem8)
                self.horizontalLayout_4.addLayout(self.verticalLayout_12)
                self.verticalLayout_15 = QtWidgets.QVBoxLayout()
                self.verticalLayout_15.setObjectName("verticalLayout_15")
                self.label_asis_cont_PIP = QtWidgets.QLabel(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.label_asis_cont_PIP.setFont(font)
                self.label_asis_cont_PIP.setAlignment(QtCore.Qt.AlignCenter)
                self.label_asis_cont_PIP.setObjectName("label_asis_cont_PIP")
                self.verticalLayout_15.addWidget(self.label_asis_cont_PIP)
                self.spinBox_asis_cont_PIP = QtWidgets.QSpinBox(self.pressure_assit_tab)
                self.spinBox_asis_cont_PIP.setMinimumSize(QtCore.QSize(0, 30))
                font = QtGui.QFont()
                font.setPointSize(27)
                self.spinBox_asis_cont_PIP.setFont(font)
                self.spinBox_asis_cont_PIP.setStyleSheet("QSpinBox::up-button { width: 32px; }\n"
                        "QSpinBox::down-button { width: 32px; }")
                self.spinBox_asis_cont_PIP.setAlignment(QtCore.Qt.AlignCenter)
                self.spinBox_asis_cont_PIP.setMinimum(10)
                self.spinBox_asis_cont_PIP.setMaximum(30)
                self.spinBox_asis_cont_PIP.setProperty("value", 20)
                self.spinBox_asis_cont_PIP.setObjectName("spinBox_asis_cont_PIP")
                self.verticalLayout_15.addWidget(self.spinBox_asis_cont_PIP)
                spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout_15.addItem(spacerItem9)
                self.horizontalLayout_4.addLayout(self.verticalLayout_15)
                self.verticalLayout_23.addLayout(self.horizontalLayout_4)
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.button_asis_cont_start = QtWidgets.QPushButton(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_asis_cont_start.setFont(font)
                self.button_asis_cont_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.button_asis_cont_start.setStyleSheet("background-color: rgb(169, 160, 157);")
                self.button_asis_cont_start.setObjectName("button_asis_cont_start")
                self.horizontalLayout.addWidget(self.button_asis_cont_start)
                self.button_asis_cont_update = QtWidgets.QPushButton(self.pressure_assit_tab)
                self.button_asis_cont_update.setEnabled(False)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_asis_cont_update.setFont(font)
                self.button_asis_cont_update.setStyleSheet("background-color: rgb(255, 160, 80);")
                self.button_asis_cont_update.setObjectName("button_asis_cont_update")
                self.horizontalLayout.addWidget(self.button_asis_cont_update)
                self.button_asis_cont_stop = QtWidgets.QPushButton(self.pressure_assit_tab)
                font = QtGui.QFont()
                font.setPointSize(25)
                self.button_asis_cont_stop.setFont(font)
                self.button_asis_cont_stop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.button_asis_cont_stop.setStyleSheet("background-color: rgb(222, 0, 0);")
                self.button_asis_cont_stop.setObjectName("button_asis_cont_stop")
                self.horizontalLayout.addWidget(self.button_asis_cont_stop)
                self.verticalLayout_23.addLayout(self.horizontalLayout)
                self.gridLayout_2.addLayout(self.verticalLayout_23, 0, 0, 1, 1)
                self.tab_widget_modes.addTab(self.pressure_assit_tab, "")
                self.gridLayout_3.addWidget(self.tab_widget_modes, 1, 1, 1, 2)
                self.frame_top_right_labels = QtWidgets.QFrame(self.centralwidget)
                self.frame_top_right_labels.setMinimumSize(QtCore.QSize(155, 450))
                self.frame_top_right_labels.setMaximumSize(QtCore.QSize(190, 700))
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(177, 202, 136))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
                self.frame_top_right_labels.setPalette(palette)
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.frame_top_right_labels.setFont(font)
                self.frame_top_right_labels.setStyleSheet("background-color:rgb(177, 202, 136);\n"
                        "")
                self.frame_top_right_labels.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_top_right_labels.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_top_right_labels.setObjectName("frame_top_right_labels")
                self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_top_right_labels)
                self.gridLayout_5.setObjectName("gridLayout_5")
                self.verticalLayout_24 = QtWidgets.QVBoxLayout()
                self.verticalLayout_24.setObjectName("verticalLayout_24")
                self.verticalLayout_9 = QtWidgets.QVBoxLayout()
                self.verticalLayout_9.setObjectName("verticalLayout_9")
                self.label_PIP = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_PIP.setFont(font)
                self.label_PIP.setAlignment(QtCore.Qt.AlignCenter)
                self.label_PIP.setObjectName("label_PIP")
                self.verticalLayout_9.addWidget(self.label_PIP)
                self.label_PIP_value = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_PIP_value.setFont(font)
                self.label_PIP_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_PIP_value.setObjectName("label_PIP_value")
                self.verticalLayout_9.addWidget(self.label_PIP_value)
                self.label_PIP_unit = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(18)
                font.setBold(False)
                font.setWeight(50)
                self.label_PIP_unit.setFont(font)
                self.label_PIP_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_PIP_unit.setObjectName("label_PIP_unit")
                self.verticalLayout_9.addWidget(self.label_PIP_unit)
                self.verticalLayout_24.addLayout(self.verticalLayout_9)
                self.line_6 = QtWidgets.QFrame(self.frame_top_right_labels)
                self.line_6.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_6.setObjectName("line_6")
                self.verticalLayout_24.addWidget(self.line_6)
                self.verticalLayout_10 = QtWidgets.QVBoxLayout()
                self.verticalLayout_10.setObjectName("verticalLayout_10")
                self.label_plateau = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_plateau.setFont(font)
                self.label_plateau.setAlignment(QtCore.Qt.AlignCenter)
                self.label_plateau.setObjectName("label_plateau")
                self.verticalLayout_10.addWidget(self.label_plateau)
                self.label_plateau_value = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_plateau_value.setFont(font)
                self.label_plateau_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_plateau_value.setObjectName("label_plateau_value")
                self.verticalLayout_10.addWidget(self.label_plateau_value)
                self.label_plateau_unit = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_plateau_unit.setFont(font)
                self.label_plateau_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_plateau_unit.setObjectName("label_plateau_unit")
                self.verticalLayout_10.addWidget(self.label_plateau_unit)
                self.verticalLayout_24.addLayout(self.verticalLayout_10)
                self.line_7 = QtWidgets.QFrame(self.frame_top_right_labels)
                self.line_7.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_7.setObjectName("line_7")
                self.verticalLayout_24.addWidget(self.line_7)
                self.verticalLayout_11 = QtWidgets.QVBoxLayout()
                self.verticalLayout_11.setObjectName("verticalLayout_11")
                self.label_mean = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_mean.setFont(font)
                self.label_mean.setAlignment(QtCore.Qt.AlignCenter)
                self.label_mean.setObjectName("label_mean")
                self.verticalLayout_11.addWidget(self.label_mean)
                self.label_mean_value = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_mean_value.setFont(font)
                self.label_mean_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_mean_value.setObjectName("label_mean_value")
                self.verticalLayout_11.addWidget(self.label_mean_value)
                self.label_mean_unit = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_mean_unit.setFont(font)
                self.label_mean_unit.setAlignment(QtCore.Qt.AlignCenter)
                self.label_mean_unit.setObjectName("label_mean_unit")
                self.verticalLayout_11.addWidget(self.label_mean_unit)
                self.verticalLayout_24.addLayout(self.verticalLayout_11)
                self.line_8 = QtWidgets.QFrame(self.frame_top_right_labels)
                self.line_8.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_8.setObjectName("line_8")
                self.verticalLayout_24.addWidget(self.line_8)
                self.verticalLayout_2 = QtWidgets.QVBoxLayout()
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.label_PEEP = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_PEEP.setFont(font)
                self.label_PEEP.setAlignment(QtCore.Qt.AlignCenter)
                self.label_PEEP.setObjectName("label_PEEP")
                self.verticalLayout_2.addWidget(self.label_PEEP)
                self.label_PEEP_value = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_PEEP_value.setFont(font)
                self.label_PEEP_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_PEEP_value.setObjectName("label_PEEP_value")
                self.verticalLayout_2.addWidget(self.label_PEEP_value)
                self.label_mean_unit_2 = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_mean_unit_2.setFont(font)
                self.label_mean_unit_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_mean_unit_2.setObjectName("label_mean_unit_2")
                self.verticalLayout_2.addWidget(self.label_mean_unit_2)
                self.verticalLayout_24.addLayout(self.verticalLayout_2)
                self.line = QtWidgets.QFrame(self.frame_top_right_labels)
                self.line.setStyleSheet("background-color: rgb(0, 0, 0);")
                self.line.setFrameShape(QtWidgets.QFrame.HLine)
                self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line.setObjectName("line")
                self.verticalLayout_24.addWidget(self.line)
                self.verticalLayout_13 = QtWidgets.QVBoxLayout()
                self.verticalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
                self.verticalLayout_13.setObjectName("verticalLayout_13")
                self.label_IE = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.label_IE.setFont(font)
                self.label_IE.setAlignment(QtCore.Qt.AlignCenter)
                self.label_IE.setObjectName("label_IE")
                self.verticalLayout_13.addWidget(self.label_IE)
                self.label_IE_value = QtWidgets.QLabel(self.frame_top_right_labels)
                font = QtGui.QFont()
                font.setFamily(".SF NS Text")
                font.setPointSize(23)
                font.setBold(True)
                font.setWeight(75)
                self.label_IE_value.setFont(font)
                self.label_IE_value.setAlignment(QtCore.Qt.AlignCenter)
                self.label_IE_value.setObjectName("label_IE_value")
                self.verticalLayout_13.addWidget(self.label_IE_value)
                self.verticalLayout_24.addLayout(self.verticalLayout_13)
                self.gridLayout_5.addLayout(self.verticalLayout_24, 0, 0, 1, 1)
                self.gridLayout_3.addWidget(self.frame_top_right_labels, 0, 2, 1, 1)
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 22))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)
                #Connect the event of the buttons being clicked with the corresponding functions. 
                self.button_cont_mand_asist_start.clicked.connect(self.pressed_cont_mand_asist_start)
                self.button_cont_mand_asist_stop.clicked.connect(self.pressed_cont_mand_asist_stop)
                self.button_asis_cont_start.clicked.connect(self.pressed_asis_cont_start)
                self.button_asis_cont_stop.clicked.connect(self.pressed_asis_cont_stop)
                self.button_patient_settings.clicked.connect(self.openpatientSettings)
                self.button_flowcalculator.clicked.connect(self.openFlowCalculator)
                self.button_alarm.clicked.connect(self.reset_alarm)
                self.button_cont_mand_asist_update.clicked.connect(self.pressed_cont_mand_asist_update)
                self.button_asis_cont_update.clicked.connect(self.pressed_asis_cont_update)
                #Setup for alarm system
                GPIO.setwarnings(False)#Disable warnings (optional)
                GPIO.setmode(GPIO.BCM)#Select GPIO mode
                self.buzzer=22#Set buzzer, in this case, pin 23 as output
                GPIO.setup(self.buzzer,GPIO.OUT)
                #Initialize variables
                self.threadpool = QThreadPool()
                self.threadflag = 0
                self.frequency_value_input = 0
                self.tidal_vol_volume_input = 0
                self.insp_pause_input = 0
                self.i_e_value_input = 0
                self.pip_value_input = 0
                self.trigger_value_input = 0
                self.time_array = [] 
                self.array_pressure = [] 
                self.array_volume = []
                self.array_flow = [] 
                ############################IMPORTANT TO CHANGE THE ARDUINO ID TO THE ONE THAT YOU ARE USING#################################
                self.arduino_id = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_75736303236351606110-if00'
                ############################IMPORTANT TO CHANGE THE ARDUINO ID TO THE ONE THAT YOU ARE USING#################################

                print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount()) #Know the amount of threads available in the machine
                self.retranslateUi(MainWindow)
                self.tab_widget_modes.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                """This method retranslateUi() sets the text and titles of the widgets."""
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "ATMO-Vent"))
                self.label_frequency.setText(_translate("MainWindow", "Frequency"))
                self.label_frequency_value.setText(_translate("MainWindow", "22"))
                self.label_frequency_unit.setText(_translate("MainWindow", "bpm"))
                self.label_tidal_vol.setText(_translate("MainWindow", "    Tidal Volume "))
                self.label_tidal_vol_value.setText(_translate("MainWindow", "450"))
                self.label_tidal_vol_unit.setText(_translate("MainWindow", "mL"))
                self.label_min_vent.setText(_translate("MainWindow", "Min. Ventilation"))
                self.label_min_vent_value.setText(_translate("MainWindow", "10.8"))
                self.label_min_vent_unit.setText(_translate("MainWindow", "L/min"))
                self.label_resistance.setText(_translate("MainWindow", "Resistance"))
                self.label_resistance_value.setText(_translate("MainWindow", "450"))
                self.label_resistance_unit.setText(_translate("MainWindow", "<html><head/><body><p>cm H<span style=\" vertical-align:sub;\">2</span>O/L/sec</p></body></html>"))
                self.label_complains.setText(_translate("MainWindow", "Complains"))
                self.label_complains_value.setText(_translate("MainWindow", "450"))
                self.label_complains_unit.setText(_translate("MainWindow", "<html><head/><body><p>ml/cm H<span style=\" vertical-align:sub;\">2</span>O</p></body></html>"))
                self.label_x_axis.setText(_translate("MainWindow", "Time [s]"))
                self.button_patient_settings.setText(_translate("MainWindow", "PATIENT \n"
                        " SETTINGS"))
                self.button_flowcalculator.setText(_translate("MainWindow", "FLOW \n"
                        " CALCULATOR"))
                self.label_cont_mand_vent_frequency.setText(_translate("MainWindow", "Frequency"))
                self.label_cont_mand_vent_tid_vol.setText(_translate("MainWindow", "Tidal Volume"))
                self.label_cont_mand_vent_insp_pause.setText(_translate("MainWindow", "Insp. Pause"))
                self.label_cont_mand_vent_I_E.setText(_translate("MainWindow", "I:E:1."))
                self.label_cont_mand_vent_PIP.setText(_translate("MainWindow", "PIP"))
                self.button_cont_mand_asist_start.setText(_translate("MainWindow", "START"))
                self.button_cont_mand_asist_stop.setText(_translate("MainWindow", "STOP"))
                self.tab_widget_modes.setTabText(self.tab_widget_modes.indexOf(self.volume_assist_tab), _translate("MainWindow", "Cont. Mand. Vent. (CMV)"))
                self.label_asis_cont_frequency.setText(_translate("MainWindow", "Frequency"))
                self.button_cont_mand_asist_update.setText(_translate("MainWindow", "UPDATE"))
                self.button_asis_cont_update.setText(_translate("MainWindow", "UPDATE"))
                self.label_asis_cont_tid_vol.setText(_translate("MainWindow", "Tidal Volume"))
                self.label_asis_cont_insp_pause.setText(_translate("MainWindow", "Insp. Pause"))
                self.label_asis_cont_trigger.setText(_translate("MainWindow", "Trigger"))
                self.radioButton_pressure.setText(_translate("MainWindow", "Pressure"))
                self.radioButton_flow.setText(_translate("MainWindow", "Flow"))
                self.label_asis_cont_PIP.setText(_translate("MainWindow", "PIP"))
                self.button_asis_cont_start.setText(_translate("MainWindow", "START"))
                self.button_asis_cont_stop.setText(_translate("MainWindow", "STOP"))
                self.tab_widget_modes.setTabText(self.tab_widget_modes.indexOf(self.pressure_assit_tab), _translate("MainWindow", "Assisted Control (AC)"))
                self.label_PIP.setText(_translate("MainWindow", "PIP"))
                self.label_PIP_value.setText(_translate("MainWindow", "450"))
                self.label_PIP_unit.setText(_translate("MainWindow", "<html><head/><body><p>cm H<span style=\" vertical-align:sub;\">2</span>O</p></body></html>"))
                self.label_plateau.setText(_translate("MainWindow", "Plateau"))
                self.label_plateau_value.setText(_translate("MainWindow", "27"))
                self.label_plateau_unit.setText(_translate("MainWindow", "<html><head/><body><p>cm H<span style=\" vertical-align:sub;\">2</span>O</p></body></html>"))
                self.label_mean.setText(_translate("MainWindow", "Mean"))
                self.label_mean_value.setText(_translate("MainWindow", "18"))
                self.label_mean_unit.setText(_translate("MainWindow", "<html><head/><body><p>cm H<span style=\" vertical-align:sub;\">2</span>O</p></body></html>"))
                self.label_PEEP.setText(_translate("MainWindow", "PEEP"))
                self.label_PEEP_value.setText(_translate("MainWindow", "0.0"))
                self.label_mean_unit_2.setText(_translate("MainWindow", "<html><head/><body><p>cm H<span style=\" vertical-align:sub;\">2</span>O</p></body></html>"))
                self.label_IE.setText(_translate("MainWindow", "I:E"))
                self.label_IE_value.setText(_translate("MainWindow", "1:2.5"))

        def read_patient_settings(self, value):
                """
                Read values from the patient settings window and calculate the Tidal volume. The values are given through the 
                thread-safe pyqtSignal() function.
                """
                self.list_hei_age_gen_vol = (list(map(str, value.split(','))))
                if self.list_hei_age_gen_vol[3] == "Male":
                        self.predicted_body_weight = 50 + 0.91 * (int(self.list_hei_age_gen_vol[0]) - 152.4)
                elif self.list_hei_age_gen_vol[3] == "Female":
                        self.predicted_body_weight = 45.5 + 0.91 * (int(self.list_hei_age_gen_vol[0]) - 152.4)
                self.tidal_volume_age_hei_gen_vol = int(self.predicted_body_weight * int(self.list_hei_age_gen_vol[2]))
                self.patient_settings_window.hide()
                self.label_tidal_vol_value.setText(str(self.tidal_volume_age_hei_gen_vol))

        def pressed_cont_mand_asist_start(self):
                """
                Configuration for START button inside the continuos mandatory ventilation tab section.
                """
                #Read values from each spinbox inside the continuos mandatory ventilation tab.
                self.frequency_value_input = (self.spinBox_cont_mand_vent_freq_value.value())
                self.tidal_vol_volume_input = (self.spinBox_cont_mand_vent_tid_vol_value.value())
                self.insp_pause_input = (self.doubleSpinBox_cont_mand_vent_insp_pause_value.value())
                self.i_e_value_input = (self.spinBox_cont_mand_vent_I_E_value.value())
                self.pip_value_input = (self.spinBox_cont_mand_vent_PIP_value.value())
                #Concatenate each value, and set it up as the Arduino is expecting to read it.
                write_Arduino = ('C,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                str(self.i_e_value_input)+','+str(self.pip_value_input)+'\n')
                #We open the serial port using the Arduinos ID instead of the machines port number, letting us use the hardware in any machine. 
                #Everytime you use a new hardware or change arduino, you have to change the ID number.
                self.arduino_controller = serial.Serial(self.arduino_id, 115200, timeout=1)
                time.sleep(1) #Wait one second to make sure that the connection was established
                self.arduino_controller.write(write_Arduino.encode('utf-8')) #Write to the arduino the concatenated string 
                #Update the values in the GUI
                self.label_frequency_value.setText(str(self.frequency_value_input))
                self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                self.label_IE_value.setText("1:2."+str(self.i_e_value_input))
                self.label_PIP_value.setText(str(self.pip_value_input))
                self.button_cont_mand_asist_start.setStyleSheet("background-color: rgb(177, 202, 136);")
                self.start_time = time.time() #Start the current time when we push start to keep track of the time in the plots (updating every 10 seconds)
                self.threadflag = 0 #This flag will later be set to 1 when we want to stop the thread.
                self.button_cont_mand_asist_update.setEnabled(True) #Enable the UPDATE button
                self.button_cont_mand_asist_start.setEnabled(False) #Disable the START button once its pushed
                self.sendThread() #Start the sendThread() function 

        def pressed_cont_mand_asist_stop(self):
                """
                Configuration for the STOP button inside the continuos mandatory ventilation tab section
                """
                self.threadflag = 1 #Update the threadflag variable to stop the current thread in the while loop in readArduino() function
                #Clear all the plots
                self.graphicsView_pressure.clear() 
                self.graphicsView_volume.clear()
                self.graphicsView_flow.clear()
                #Update GUI
                self.button_cont_mand_asist_start.setStyleSheet("background-color: rgb(169, 160, 157);") #Update the color button for START
                self.button_cont_mand_asist_update.setEnabled(False)
                self.button_cont_mand_asist_start.setEnabled(True)
                time.sleep(0.5) #Wait for half a second until the thread stops correctly

        def pressed_cont_mand_asist_update(self):
                """
                Configuration for UPDATE button inside the continuos mandatory ventilation tab section.
                """
                #Read values from each spinbox inside the continuos mandatory ventilation tab.
                self.frequency_value_input = (self.spinBox_cont_mand_vent_freq_value.value())
                self.tidal_vol_volume_input = (self.spinBox_cont_mand_vent_tid_vol_value.value())
                self.insp_pause_input = (self.doubleSpinBox_cont_mand_vent_insp_pause_value.value())
                self.i_e_value_input = (self.spinBox_cont_mand_vent_I_E_value.value())
                self.pip_value_input = (self.spinBox_cont_mand_vent_PIP_value.value())
                #Concatenate each value, and set it up as the Arduino is expecting to read it.
                write_Arduino = ('22C,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                str(self.i_e_value_input)+','+str(self.pip_value_input)+'\n')
                self.arduino_controller.write(write_Arduino.encode('utf-8')) #Write to the arduino
                #Update the values in the GUI
                self.label_frequency_value.setText(str(self.frequency_value_input))
                self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                self.label_IE_value.setText("1:2."+str(self.i_e_value_input))
                self.label_PIP_value.setText(str(self.pip_value_input))
                

        def pressed_asis_cont_start(self):
                """
                Configuration for START BUTTON inside the assisted control tab section
                """
                #Read values from each spinbox inside the assisted control tab.
                self.frequency_value_input = (self.spinBox_asis_cont_frequency.value())
                self.tidal_vol_volume_input = (self.spinBox_asis_cont_tid_vol.value())
                self.insp_pause_input = (self.doubleSpinBox_insp_pause.value())
                self.trigger_value_input = (self.spinBox_asis_cont_trigger_pre_flow.value())
                self.pip_value_input = (self.spinBox_asis_cont_PIP.value())

                if self.radioButton_pressure.isChecked(): #In case Pressure trigger mode is selected
                        #Concatenate each value, and set it up as the Arduino is expecting to read it.
                        write_Arduino = ('P,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                        str(self.trigger_value_input)+','+str(self.pip_value_input)+'\n')
                        #We open the serial port using the Arduinos ID instead of the machines port number, letting us use the hardware in any machine. 
                        #Everytime you use a new hardware or change arduino, you have to change the ID number.
                        self.arduino_controller = serial.Serial(self.arduino_id, 115200, timeout=1)  #RPI
                        time.sleep(1) #Wait one second to make sure that the connection was established
                        self.arduino_controller.write(write_Arduino.encode('utf-8')) #Write to the Arduino

                        #Update the values in the GUI
                        self.label_frequency_value.setText(str(self.frequency_value_input))
                        self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                        self.label_PIP_value.setText(str(self.pip_value_input))
                        self.button_asis_cont_start.setStyleSheet("background-color: rgb(177, 202, 136);")
                        self.start_time = time.time() #Start the current time when we push start to keep track of the time in the plots (updating every 10 seconds)
                        self.threadflag = 0#This flag will later be set to 1 when we want to stop the thread.
                        self.button_asis_cont_update.setEnabled(True)#Enable the UPDATE button
                        self.button_asis_cont_start.setEnabled(False)#Disable the START button once its pushed
                        self.sendThread()#Start the sendThread() function 

                elif self.radioButton_flow.isChecked(): #In case Flow trigger mode is selected
                        #Concatenate each value, and set it up as the Arduino is expecting to read it.
                        write_Arduino = ('F,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                        str(self.trigger_value_input)+','+str(self.pip_value_input)+'\n')
                        #We open the serial port using the Arduinos ID instead of the machines port number, letting us use the hardware in any machine. 
                        #Everytime you use a new hardware or change arduino, you have to change the ID number.
                        self.arduino_controller = serial.Serial(self.arduino_id, 115200, timeout=1)  #RPI
                        time.sleep(1) #Wait one second to make sure that the connection was established
                        self.arduino_controller.write(write_Arduino.encode('utf-8'))#Write to the Arduino

                        #Update the values in the GUI
                        self.label_frequency_value.setText(str(self.frequency_value_input))
                        self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                        self.label_PIP_value.setText(str(self.pip_value_input))
                        self.button_asis_cont_start.setStyleSheet("background-color: rgb(177, 202, 136);")
                        self.start_time = time.time() #Start the current time when we push start to keep track of the time in the plots (updating every 10 seconds)
                        self.threadflag = 0#This flag will later be set to 1 when we want to stop the thread.
                        self.button_asis_cont_update.setEnabled(True)#Enable the UPDATE button
                        self.button_asis_cont_start.setEnabled(False)#Disable the START button once its pushed
                        self.sendThread()#Start the sendThread() function 
                        
                else: #In case no trigger mode was selected, pop-up message
                        QtWidgets.QMessageBox.information(QtWidgets.QMainWindow(), "Attention!","You have to select a trigger mode", QtWidgets.QMessageBox.Ok)

        #Configuration for STOP BUTTON inside the assisted control tab section
        def pressed_asis_cont_stop(self):
                """
                Configuration for STOP BUTTON inside the assisted control tab section
                """
                self.threadflag = 1 #Update the threadflag variable to stop the current thread in the while loop in readArduino() function
                #Clear all the plots
                self.graphicsView_pressure.clear()
                self.graphicsView_volume.clear()
                self.graphicsView_flow.clear()
                #Update GUI
                self.button_asis_cont_start.setStyleSheet("background-color: rgb(169, 160, 157);")  #Update the color button for START
                self.button_asis_cont_update.setEnabled(False)
                self.button_asis_cont_start.setEnabled(True)
                time.sleep(0.5) #Wait for half a second until the thread stops correctly

        def pressed_asis_cont_update(self):
                """
                Configuration for UPDATE button inside the assisted control tab section.
                """
                #Read values from each spinbox inside the assisted control tab.
                self.frequency_value_input = (self.spinBox_asis_cont_frequency.value())
                self.tidal_vol_volume_input = (self.spinBox_asis_cont_tid_vol.value())
                self.insp_pause_input = (self.doubleSpinBox_insp_pause.value())
                self.trigger_value_input = (self.spinBox_asis_cont_trigger_pre_flow.value())
                self.pip_value_input = (self.spinBox_asis_cont_PIP.value())

                if self.radioButton_pressure.isChecked(): #In case Pressure trigger mode is selected
                        #Concatenate each value, and set it up as the Arduino is expecting to read it.
                        write_Arduino = ('P,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                        str(self.trigger_value_input)+','+str(self.pip_value_input)+'\n')
                        self.arduino_controller.write(write_Arduino.encode('utf-8'))#Write to the Arduino
                        #Update the values in the GUI
                        self.label_frequency_value.setText(str(self.frequency_value_input))
                        self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                        self.label_PIP_value.setText(str(self.pip_value_input))
                        
                elif self.radioButton_flow.isChecked():#In case Flow trigger mode is selected
                        #Join each value, and set it up as the Arduino is expecting to read it.
                        write_Arduino = ('F,'+str(self.frequency_value_input)+','+str(self.tidal_vol_volume_input) + ','+str(self.insp_pause_input)+','+
                        str(self.trigger_value_input)+','+str(self.pip_value_input)+'\n')
                        print(write_Arduino.encode('utf-8'))
                        self.arduino_controller.write(write_Arduino.encode('utf-8'))#Write to the Arduino
                        #Update the values in the GUI
                        self.label_frequency_value.setText(str(self.frequency_value_input))
                        self.label_tidal_vol_value.setText(str(self.tidal_vol_volume_input))
                        self.label_PIP_value.setText(str(self.pip_value_input))
                else: #In case no radio button was selected, pop-up message
                        QtWidgets.QMessageBox.information(QtWidgets.QMainWindow(), "Attention!","You have to select a trigger mode", QtWidgets.QMessageBox.Ok)

        def readArduino(self, progress_callback):
                """
                This function will be executed continuously in a new thread different from the main one where the UI is running. This way the GUI will be responsive
                while the readArduino() function is continuosly plotting new data in the graphs.
                """
                self.data_line_pressure =  self.graphicsView_pressure.plot(self.time_array, self.array_pressure, pen=pg.mkPen('r', width=1))
                self.data_line_volume =  self.graphicsView_volume.plot(self.time_array, self.array_volume, pen=pg.mkPen('g', width=1))
                self.data_line_flow =  self.graphicsView_flow.plot(self.time_array, self.array_flow, pen=pg.mkPen('y', width=1))
                #Initialize variables
                i=0
                flag = 0
                value_str = "1" #Value that we have to send to the Arduino in order for it to send data
                self.arduino_controller.flushInput() #At this point we have to flush the input buffer, discarding all its contents. To be sure that there is not any previous caracter

                while True:
                        time.sleep(0.06) # We take 6 ms between each value. Due to RPI
                        if flag < 2:
                                #We need to make sure that Arduino is sending reliable data, therefore, we wait for it to send two values and then keep reading continuosly
                                self.arduino_controller.write(value_str.encode('utf-8')) #Write "1" to the Arduino to receive data from it.
                                arduinoString_noDecode = self.arduino_controller.readline()
                                flag += 1
                                continue
                        try:
                                self.arduino_controller.write(value_str.encode('utf-8')) #Write "1" to the Arduino to receive data from it.
                                arduinoString = self.arduino_controller.readline().decode("utf-8").rstrip("\n") #read the text line from serial port and decode from byte format to ASCII
                                self.arduino_list = (list(map(str, arduinoString.split(',')))) #Split by commas the received text by the arduino and map them all as Strings
                                if len(self.arduino_list) != 9: # The expected amount of value to be received is 9, therefore, if it is different to 9, we will wait for the next line
                                        continue
                                #Safe each value from the received list to a corresponding variable.
                                self.pressure_cm = float(self.arduino_list[0])
                                self.flow_lpm = float(self.arduino_list[1])
                                self.volume_value = float(self.arduino_list[2])
                                self.frequency = float(self.arduino_list[3]) # Units:bpm
                                self.IE_value = float(self.arduino_list[4])
                                self.pip_value = float(self.arduino_list[5]) #Units:cm H2O
                                self.plateau_value = float(self.arduino_list[6])
                                self.peep_value = float(self.arduino_list[7]) #Units:cm H2O
                                self.error_pvf = (self.arduino_list[8]) #This values will indicate if there is an error with pressure, volume or flow. If everything is fine it should be "000"
                                                                        #but if pressure fails then we will receive "P00", if volume "0V0", if flow "00F", if all "PVF"
                                self.mean_value = round(0.5 * (self.pip_value - self.peep_value) * (1/self.IE_value)+self.peep_value,2)
                                self.compliance_value = round(self.volume_value / (self.plateau_value - self.peep_value),2) # ml/cm H2O
                                self.min_ventilation_value = round(self.volume_value * self.frequency /1000,2) #L/min
                                # self.resistance_value = round((self.pip_value - self.plateau_value)*60/max(list_flow),2) #cm H2O/L/sec
                                #Update GUI values
                                self.label_frequency_value.setText(str(round(self.frequency,2)))
                                self.label_tidal_vol_value.setText(str(round(self.volume_value,2)))
                                self.label_PIP_value.setText(str(self.pip_value))
                                self.label_plateau_value.setText(str(self.plateau_value))
                                self.label_PEEP_value.setText(str(self.peep_value))
                                self.label_IE_value.setText(str(self.IE_value))
                                self.label_min_vent_value.setText(str(self.min_ventilation_value))
                                self.label_complains_value.setText(str(self.compliance_value))
                                self.label_mean_value.setText(str(self.mean_value))
                                # self.label_resistance_value.setText(str(self.resistance_value))

                                if self.pip_value > float(self.pip_value_input) or self.volume_value < self.tidal_vol_volume_input or abs(self.volume_value - self.tidal_vol_volume_input) > 20 or abs(self.IE_value - self.i_e_value_input)>0.2 :
                                        #If any of it is True, then, turn on the alarm. 
                                        GPIO.output(self.buzzer,GPIO.HIGH)
                                        self.spinBox_cont_mand_vent_PIP_value.setStyleSheet('QLabel#nom_plan_label {color: red}')#change value to red
                                
                                if self.error_pvf != "000": #if the salf value is different from "000" (pressure, volume and flow correct) then, turn alarm ON. 
                                        GPIO.output(self.buzzer,GPIO.HIGH)

                        except Exception as e: #If there is any error, the system must keep working, therefore, we print the error of the error that the user made for them to fix
                                                #but the system will still keep working.
                                print(e)
                                continue
                        progress_callback.emit(arduinoString) #What we want to send as a callback during the execution of the thread
                        if self.threadflag == 1:
                                self.threadflag = 0
                                break
        def reset_alarm(self):#This function will be called when the self.button_alarm button is pushed. It will reset the alarm.
                GPIO.output(self.buzzer,GPIO.LOW)#Turn off the alarm noise
                #Set the possible failures to black
                self.spinBox_cont_mand_vent_PIP_value.setStyleSheet('QLabel#nom_plan_label {color: black}') 
                self.spinBox_cont_mand_vent_freq_value.setStyleSheet('QLabel#nom_plan_label {color: black}') 
                self.spinBox_cont_mand_vent_tid_vol_value.setStyleSheet('QLabel#nom_plan_label {color: black}')


        def update_plot_data(self): 
                """
                This function is called by the progress_fn() function. It will be updated constantly while the thread is running and readArduino() 
                function is receiving new values. It will store data for 10 seconds and then it will be updating the plot removing the first element
                of the Array and adding one at the end.
                """
                
                if (time.time() - self.start_time > 10): #Once it has stored data for 10 seconds, starts to update.
                        # Remove the first element (updating values)
                        self.time_array = self.time_array[1:]
                        self.array_pressure = self.array_pressure[1:] 
                        self.array_volume = self.array_volume[1:] 
                        self.array_flow = self.array_flow[1:] 
                # Add a new measured value. (By default appends at the end)
                self.array_pressure.append(self.pressure_cm) 
                self.array_volume.append(self.volume_value)  
                self.array_flow.append(self.flow_lpm) 
                self.time_array.append(time.time() - self.start_time)
                # Update the plot with the new pressure, flow and volume data.
                self.data_line_pressure.setData(self.time_array, self.array_pressure, pen=pg.mkPen('r', width=1))  
                self.data_line_flow.setData(self.time_array, self.array_flow, pen=pg.mkPen('g', width=1))  
                self.data_line_volume.setData(self.time_array, self.array_volume, pen=pg.mkPen('y', width=1))

        def thread_complete(self):
                """
                This function is executed once the thread is ended (when the self.threadflag!=0). It will clear all the arrays,
                flush the input left in the serial communication and send to the Arduino the stop command, and close the serial
                communication.
                """
                self.array_pressure.clear() 
                self.array_volume.clear()
                self.array_flow.clear() 
                self.time_array.clear() 
                self.arduino_controller.flushInput()
                write_Arduino = ('22'+'\n')
                self.arduino_controller.write(write_Arduino.encode('utf-8'))
                self.arduino_controller.close()

        def progress_fn(self, value):
                """
                This function tracks the progress and will stop when the thread is completed. It is controlled by the pyqtSignal() function 
                from the WorkerSignals class. Thius function will check that the Arduino sent the expected amount of values (9) and that 
                the main values (pressure, flow and volume) are not empty and call the function that will update the plots.
                """
                if len(self.arduino_list) ==9 and self.pressure_cm != ""and self.flow_lpm != "" and self.volume_value!="":  
                        self.update_plot_data()



        def sendThread(self):
                """
                This function is the responsible one to initialize the threads and connect the signals to the corresponding functions. 
                """
                #Pass the function to execute
                self.worker = Worker(self.readArduino)
                #Connect the worker handler functions to these signals to receive notification of completion and the result of threads.
                self.worker.signals.finished.connect(self.thread_complete)
                self.worker.signals.progress.connect(self.progress_fn)
                # Execute self.worker 
                self.threadpool.start(self.worker) 

"""
Initialization of the app
"""
import pyqtgraph as pg
import serial
import time
import _thread
import subprocess

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
