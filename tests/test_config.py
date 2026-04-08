import os
import json
from src.config import Config

def test_config_save_load():
	config = Config()
	config.FILE_PATH = "test_config.json"
	config.units = "in"
	config.origin = "bottom_right"
	config.dpi_x = 120.0
	config.save()
	
	new_config = Config()
	new_config.FILE_PATH = "test_config.json"
	new_config.load()
	
	assert new_config.units == "in"
	assert new_config.origin == "bottom_right"
	assert new_config.dpi_x == 120.0
	
	# Cleanup
	if os.path.exists("test_config.json"):
		os.remove("test_config.json")
