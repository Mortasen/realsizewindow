import sys
from PyQt6.QtWidgets import QApplication
from realsizewindow.config import config
from realsizewindow.gui.main_window import MainWindow
from loguru import logger

def main():
	# Configure logger
	logger.remove()
	logger.add(sys.stderr, level="INFO")
	logger.add("app.log", rotation="10 MB", level="DEBUG")
	
	app = QApplication(sys.argv)
	
	# Try to get screen DPI if not calibrated
	if not config.is_calibrated:
		screen = app.primaryScreen()
		if screen:
			config.dpi_x = screen.physicalDotsPerInchX()
			config.dpi_y = screen.physicalDotsPerInchY()
			logger.info(f"Auto-detected DPI: {config.dpi_x} x {config.dpi_y}")
	
	window = MainWindow()
	window.show()
	
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
