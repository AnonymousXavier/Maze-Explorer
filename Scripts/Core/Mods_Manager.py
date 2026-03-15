from importlib.machinery import ModuleSpec
import importlib.util
import os
import sys

class Mods_Manager:
	def __init__(self) -> None:
		self.active_entities = []
		self.loaded_mods = []

	def run(self):
		self.load_mods()
		self.unpack_attributes()

	def load_mods(self, mod_folder="mods"):
		"""Scans the mod folder and dynamically loads scripts."""
		if not os.path.exists(mod_folder):
			os.makedirs(mod_folder)
			print(f"Created '{mod_folder}' folder. Drop your mod scripts here!")
			return

		for filename in os.listdir(mod_folder):
			if filename.endswith(".py"):
				mod_name = filename[:-3]
				filepath = os.path.join(mod_folder, filename)

				# Dynamically load the python file
				spec = importlib.util.spec_from_file_location(mod_name, filepath)
				mod = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(mod)

				self.loaded_mods.append(mod)

	def unpack_attributes(self):
		# Check if the mod has the required 'Entity' class
		for mod in self.loaded_mods:
			if hasattr(mod, 'Entity'):
				entity = mod.Entity()
				self.active_entities.append(entity)
				print(f"Loaded mod: {entity.name}")