import json
import os
from loguru import logger

class Config:
	FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
	
	def __init__(self):
		self.units = "mm"  # mm, cm, in
		self.origin = "top_left"  # top_left, top_right, bottom_left, bottom_right
		self.dpi_x = 96.0
		self.dpi_y = 96.0
		self.is_calibrated = False
		self.load()

	def load(self):
		if os.path.exists(self.FILE_PATH):
			try:
				with open(self.FILE_PATH, "r") as f:
					data = json.load(f)
					self.units = data.get("units", "mm")
					self.origin = data.get("origin", "top_left")
					self.dpi_x = data.get("dpi_x", 96.0)
					self.dpi_y = data.get("dpi_y", 96.0)
					self.is_calibrated = data.get("is_calibrated", False)
					logger.info(f"Loaded config: units={self.units}, origin={self.origin}, dpi={self.dpi_x}x{self.dpi_y}")
			except Exception as e:
				logger.error(f"Failed to load config: {e}")

	def save(self):
		try:
			data = {
				"units": self.units,
				"origin": self.origin,
				"dpi_x": self.dpi_x,
				"dpi_y": self.dpi_y,
				"is_calibrated": self.is_calibrated
			}
			with open(self.FILE_PATH, "w") as f:
				json.dump(data, f, indent=4)
			logger.info(f"Saved config: {data}")
		except Exception as e:
			logger.error(f"Failed to save config: {e}")

config = Config()
