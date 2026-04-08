from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QFont, QPalette, QColor
from realsizewindow.config import config
from loguru import logger

class BaseRuler(QWidget):
	THICKNESS = 25

	def __init__(self, parent=None):
		super().__init__(parent)
		self.thickness = self.THICKNESS
		self.setAutoFillBackground(False)

	def get_colors(self):
		palette = self.palette()
		base_bg = palette.color(QPalette.ColorRole.Window)
		text_color = palette.color(QPalette.ColorRole.WindowText)
		ruler_bg = base_bg.darker(125)
		if ruler_bg == base_bg and base_bg.lightness() < 30:
			ruler_bg = QColor(max(0, base_bg.red() - 15), 
							  max(0, base_bg.green() - 15), 
							  max(0, base_bg.blue() - 15))
		return ruler_bg, text_color

	def get_ppu(self):
		unit = config.units
		unit_in_inch = 25.4 if unit == "mm" else (2.54 if unit == "cm" else 1.0)
		return config.dpi_x / unit_in_inch, config.dpi_y / unit_in_inch

	def get_divs(self):
		unit = config.units
		sub_divs = 8 if unit == "in" else (10 if unit == "cm" else 1)
		major_div = 1 if unit in ("in", "cm") else 10
		return sub_divs, major_div

	def draw_ticks(self, painter, is_horizontal, length, widget_offset, is_reversed, text_color, align_end=False, skip_zero=False):
		ppu_x, ppu_y = self.get_ppu()
		ppu = ppu_x if is_horizontal else ppu_y
		sub_divs, major_div = self.get_divs()
		
		painter.setPen(QPen(text_color, 1))
		painter.setFont(QFont("Arial", 8))
		
		start_val = widget_offset / ppu
		end_val = (widget_offset + length) / ppu
		min_i, max_i = int(start_val), int(end_val) + 1
		
		for i in range(min_i, max_i + 1):
			for j in range(sub_divs):
				if i == max_i and j > 0: break
				val = i + j/sub_divs
				if skip_zero and i == 0 and j == 0: continue
					
				pos_abs = val * ppu
				pos_rel = pos_abs - widget_offset if not is_reversed else length - (pos_abs - widget_offset)

				if 0 <= pos_rel <= length:
					is_major = (i % major_div == 0 and j == 0)
					tick_len = 15 if is_major else 8
					if not is_major and sub_divs > 1: tick_len = 5
					
					if is_horizontal:
						# If align_end is True, ticks start at self.thickness and go up (-tick_len)
						y_start = self.thickness if align_end else 0
						y_end = self.thickness - tick_len if align_end else tick_len
						painter.drawLine(int(pos_rel), y_start, int(pos_rel), y_end)
						if is_major and val >= 0:
							ty = self.thickness - 12 if align_end else 22
							painter.drawText(int(pos_rel + 2), ty, str(i))
					else:
						# If align_end is True, ticks start at self.thickness and go left (-tick_len)
						x_start = self.thickness if align_end else 0
						x_end = self.thickness - tick_len if align_end else tick_len
						painter.drawLine(x_start, int(pos_rel), x_end, int(pos_rel))
						if is_major and val >= 0:
							tx = 2 if align_end else 18
							painter.drawText(tx, int(pos_rel - 2), str(i))

class CornerWidget(BaseRuler):
	def __init__(self, position="top_left", parent=None):
		super().__init__(parent)
		self.position = position
		self.setFixedSize(self.thickness, self.thickness)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		bg, text = self.get_colors()
		painter.fillRect(self.rect(), bg)
		
		origin = config.origin
		is_origin = (self.position == origin)
		
		draw_h = draw_v = False
		if is_origin:
			draw_h = draw_v = True
		else:
			if origin == "bottom_left":
				if self.position == "top_left": draw_v = True
				elif self.position in ("bottom_right", "top_right"): draw_h = True
			elif origin == "top_left":
				if self.position == "bottom_left": draw_v = True
				elif self.position in ("top_right", "bottom_right"): draw_h = True
			elif origin == "top_right":
				if self.position == "bottom_right": draw_v = True
				elif self.position in ("top_left", "bottom_left"): draw_h = True
			elif origin == "bottom_right":
				if self.position == "top_right": draw_v = True
				elif self.position in ("bottom_left", "top_left"): draw_h = True

		window = self.window()
		w_width = window.width() if window else self.thickness
		w_height = window.height() if window else self.thickness

		if draw_h:
			is_h_reversed = ("right" in origin)
			offset_h = (0 if "left" in self.position else w_width - self.thickness) if "left" in origin else (0 if "right" in self.position else w_width - self.thickness)
			# Horizontal ticks should be on top edge for top corners, bottom edge for bottom corners
			self.draw_ticks(painter, True, self.thickness, offset_h, is_h_reversed, text, align_end=("bottom" in self.position), skip_zero=is_origin)

		if draw_v:
			is_v_reversed = ("bottom" in origin)
			offset_v = (0 if "top" in self.position else w_height - self.thickness) if "top" in origin else (0 if "bottom" in self.position else w_height - self.thickness)
			# Vertical ticks should be on left edge for left corners, right edge for right corners
			self.draw_ticks(painter, False, self.thickness, offset_v, is_v_reversed, text, align_end=("right" in self.position), skip_zero=is_origin)

		if is_origin:
			painter.setPen(QPen(text, 1))
			if self.position == "top_left": painter.drawLine(0, 0, self.thickness, self.thickness)
			elif self.position == "top_right": painter.drawLine(self.thickness, 0, 0, self.thickness)
			elif self.position == "bottom_left": painter.drawLine(0, self.thickness, self.thickness, 0)
			elif self.position == "bottom_right": painter.drawLine(self.thickness, self.thickness, 0, 0)
			
			painter.setFont(QFont("Arial", 8))
			lx = self.thickness if "right" in self.position else 0
			ly = self.thickness if "bottom" in self.position else 0
			painter.drawText(lx + 2 if "left" in self.position else lx - 10, 
							 ly + (10 if "bottom" in self.position else 22), "0")

class RulerWidget(BaseRuler):
	TOP, BOTTOM, LEFT, RIGHT = 0, 1, 2, 3

	def __init__(self, side=TOP, parent=None):
		super().__init__(parent)
		self.side = side
		if self.side in (self.TOP, self.BOTTOM): self.setFixedHeight(self.thickness)
		else: self.setFixedWidth(self.thickness)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		bg, text = self.get_colors()
		painter.fillRect(self.rect(), bg)
		
		origin = config.origin
		is_horiz = self.side in (self.TOP, self.BOTTOM)
		length = self.width() if is_horiz else self.height()
		
		if is_horiz:
			self.draw_ticks(painter, True, length, self.thickness, ("right" in origin), text, align_end=(self.side == self.BOTTOM))
		else:
			self.draw_ticks(painter, False, length, self.thickness, ("bottom" in origin), text, align_end=(self.side == self.RIGHT))
