from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPen
from src.config import config
from loguru import logger

class CalibrationBox(QFrame):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
		self.setLineWidth(2)
		self.target_mm_w = 85.6
		self.target_mm_h = 53.98
		self.dpi_x = config.dpi_x
		self.dpi_y = config.dpi_y

	def update_dpi(self, dpi_x, dpi_y):
		self.dpi_x = dpi_x
		self.dpi_y = dpi_y
		self.update()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		
		# Draw the physical-size rectangle
		# mm to pixels: (mm / 25.4) * DPI
		px_w = int((self.target_mm_w / 25.4) * self.dpi_x)
		px_h = int((self.target_mm_h / 25.4) * self.dpi_y)
		
		rect_x = (self.width() - px_w) // 2
		rect_y = (self.height() - px_h) // 2
		
		painter.setPen(QPen(QColor(0, 120, 215), 3))
		painter.drawRect(rect_x, rect_y, px_w, px_h)
		
		# Label for the user
		painter.setPen(QPen(Qt.GlobalColor.black, 1))
		painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Place Credit Card Here\n(85.6mm x 53.98mm)")

class CalibrationDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Manual Calibration")
		self.setMinimumSize(400, 300)
		self.layout = QVBoxLayout(self)
		
		self.info_label = QLabel("Adjust the DPI until the blue rectangle matches a physical credit card.")
		self.layout.addWidget(self.info_label)
		
		self.box = CalibrationBox()
		self.box.setMinimumSize(350, 200)
		self.layout.addWidget(self.box)
		
		self.controls = QHBoxLayout()
		self.controls.addWidget(QLabel("DPI:"))
		
		self.dpi_spin = QDoubleSpinBox()
		self.dpi_spin.setRange(20, 1000)
		self.dpi_spin.setValue(config.dpi_x)
		self.dpi_spin.setDecimals(1)
		self.dpi_spin.valueChanged.connect(self.on_dpi_changed)
		self.controls.addWidget(self.dpi_spin)
		
		self.layout.addLayout(self.controls)
		
		self.buttons = QHBoxLayout()
		self.save_btn = QPushButton("Save && Close")
		self.save_btn.clicked.connect(self.accept)
		self.cancel_btn = QPushButton("Cancel")
		self.cancel_btn.clicked.connect(self.reject)
		
		self.buttons.addWidget(self.save_btn)
		self.buttons.addWidget(self.cancel_btn)
		self.layout.addLayout(self.buttons)

	def on_dpi_changed(self, val):
		self.box.update_dpi(val, val)

	def get_calibrated_dpi(self):
		return self.dpi_spin.value()
