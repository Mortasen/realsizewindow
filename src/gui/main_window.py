from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
								QLabel, QDoubleSpinBox, QPushButton, QComboBox, 
								QGridLayout, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.config import config
from src.gui.rulers import RulerWidget, CornerWidget
from src.gui.calibration_dialog import CalibrationDialog
from loguru import logger

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Real Size Window")
		self.setMinimumSize(450, 300)
		
		# Main Widget and layout
		self.central_widget = QWidget()
		self.setCentralWidget(self.central_widget)
		self.main_layout = QVBoxLayout(self.central_widget)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		
		# Grid for Rulers and Content
		self.grid = QGridLayout()
		self.grid.setSpacing(0)
		self.grid.setContentsMargins(0, 0, 0, 0)
		self.main_layout.addLayout(self.grid)
		
		# Rulers and Corners
		self.top_ruler = RulerWidget(RulerWidget.TOP)
		self.bottom_ruler = RulerWidget(RulerWidget.BOTTOM)
		self.left_ruler = RulerWidget(RulerWidget.LEFT)
		self.right_ruler = RulerWidget(RulerWidget.RIGHT)
		
		self.corner_tl = CornerWidget("top_left")
		self.corner_tr = CornerWidget("top_right")
		self.corner_bl = CornerWidget("bottom_left")
		self.corner_br = CornerWidget("bottom_right")
		
		# Main area where the size is displayed
		self.content_area = QFrame()
		self.content_area.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
		self.content_layout = QVBoxLayout(self.content_area)
		
		self.center_container = QWidget()
		self.center_grid = QGridLayout(self.center_container)
		self.center_grid.setSpacing(10)
		self.center_grid.setContentsMargins(20, 20, 20, 20)
		
		# Consistent height for all interactive widgets
		WIDGET_HEIGHT = 30
		
		# Row 0: Width and Height
		self.center_grid.addWidget(QLabel("Width:"), 0, 0)
		self.w_spin = QDoubleSpinBox()
		self.w_spin.setRange(1.0, 5000)
		self.w_spin.setDecimals(1)
		self.w_spin.setFixedHeight(WIDGET_HEIGHT)
		self.w_spin.setSuffix(f" {config.units}")
		self.center_grid.addWidget(self.w_spin, 0, 1)
		
		self.center_grid.addWidget(QLabel("Height:"), 0, 2)
		self.h_spin = QDoubleSpinBox()
		self.h_spin.setRange(1.0, 5000)
		self.h_spin.setDecimals(1)
		self.h_spin.setFixedHeight(WIDGET_HEIGHT)
		self.h_spin.setSuffix(f" {config.units}")
		self.center_grid.addWidget(self.h_spin, 0, 3)
		
		self.resize_btn = QPushButton("Set Size")
		self.resize_btn.setFixedHeight(WIDGET_HEIGHT)
		self.resize_btn.setStyleSheet("font-weight: bold;")
		self.resize_btn.clicked.connect(self.apply_target_size)
		self.center_grid.addWidget(self.resize_btn, 0, 4)
		
		# Row 1: Unit and Origin
		self.center_grid.addWidget(QLabel("Unit:"), 1, 0)
		self.unit_combo = QComboBox()
		self.unit_combo.setFixedHeight(WIDGET_HEIGHT)
		self.unit_combo.addItems(["mm", "cm", "in"])
		self.unit_combo.setCurrentText(config.units)
		self.unit_combo.currentTextChanged.connect(self.change_units)
		self.center_grid.addWidget(self.unit_combo, 1, 1)
		
		self.center_grid.addWidget(QLabel("Origin:"), 1, 2)
		self.origin_combo = QComboBox()
		self.origin_combo.setFixedHeight(WIDGET_HEIGHT)
		self.origin_combo.addItems(["top_left", "top_right", "bottom_left", "bottom_right"])
		self.origin_combo.setCurrentText(config.origin)
		self.origin_combo.currentTextChanged.connect(self.change_origin)
		self.center_grid.addWidget(self.origin_combo, 1, 3)
		
		self.calibrate_btn = QPushButton("Calibrate")
		self.calibrate_btn.setFixedHeight(WIDGET_HEIGHT)
		self.calibrate_btn.clicked.connect(self.open_calibration)
		self.center_grid.addWidget(self.calibrate_btn, 1, 4)
		
		self.content_layout.addWidget(self.center_container, 0, Qt.AlignmentFlag.AlignCenter)
		
		self.setup_grid()
		
		# Initialize UI state
		self.on_config_changed()

	def setup_grid(self):
		# Corners
		self.grid.addWidget(self.corner_tl, 0, 0)
		self.grid.addWidget(self.corner_tr, 0, 2)
		self.grid.addWidget(self.corner_bl, 2, 0)
		self.grid.addWidget(self.corner_br, 2, 2)
		
		# Rulers
		self.grid.addWidget(self.top_ruler, 0, 1)
		self.grid.addWidget(self.bottom_ruler, 2, 1)
		self.grid.addWidget(self.left_ruler, 1, 0)
		self.grid.addWidget(self.right_ruler, 1, 2)
		
		# Content
		self.grid.addWidget(self.content_area, 1, 1)

	def change_units(self, text):
		config.units = text
		self.w_spin.setSuffix(f" {text}")
		self.h_spin.setSuffix(f" {text}")
		config.save()
		self.on_config_changed()

	def change_origin(self, text):
		config.origin = text
		config.save()
		# Redraw corners to update diagonal
		self.corner_tl.update()
		self.corner_tr.update()
		self.corner_bl.update()
		self.corner_br.update()
		self.on_config_changed()

	def on_config_changed(self):
		self.top_ruler.update()
		self.bottom_ruler.update()
		self.left_ruler.update()
		self.right_ruler.update()
		self.update_inputs_from_size()

	def update_inputs_from_size(self):
		# Measurement area is the entire window
		w_px = self.width()
		h_px = self.height()
		
		dpi_x = config.dpi_x
		dpi_y = config.dpi_y
		
		unit_in_inch = 25.4 if config.units == "mm" else (2.54 if config.units == "cm" else 1.0)
		w = (w_px / dpi_x) * unit_in_inch
		h = (h_px / dpi_y) * unit_in_inch
		
		# Update spin boxes
		self.w_spin.blockSignals(True)
		self.h_spin.blockSignals(True)
		self.w_spin.setValue(w)
		self.h_spin.setValue(h)
		self.w_spin.blockSignals(False)
		self.h_spin.blockSignals(False)

	def apply_target_size(self):
		w_target = self.w_spin.value()
		h_target = self.h_spin.value()
		
		dpi_x = config.dpi_x
		dpi_y = config.dpi_y
		
		unit_in_inch = 25.4 if config.units == "mm" else (2.54 if config.units == "cm" else 1.0)
		w_px_target = int((w_target / unit_in_inch) * dpi_x)
		h_px_target = int((h_target / unit_in_inch) * dpi_y)
		
		# resize() sets the content size
		self.resize(w_px_target, h_px_target)
		logger.info(f"Resizing to {w_target}x{h_target} {config.units} ({w_px_target}x{h_px_target} px)")

	def open_calibration(self):
		dlg = CalibrationDialog(self)
		if dlg.exec():
			new_dpi = dlg.get_calibrated_dpi()
			config.dpi_x = new_dpi
			config.dpi_y = new_dpi
			config.is_calibrated = True
			config.save()
			self.on_config_changed()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.update_inputs_from_size()
