import os
import importlib.util
from Misc.BaseMod import BaseMod

class ModsManager:
    active_mods = []

    @classmethod
    def load_mods(cls):
        mods_path = "mods"
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
            return

        for filename in os.listdir(mods_path):
            if filename.endswith(".py"):
                mod_name = filename[:-3]
                file_path = os.path.join(mods_path, filename)

                # 1. Load the script dynamically
                spec = importlib.util.spec_from_file_location(mod_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 2. Scan the script for classes that inherit from BaseMod
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, BaseMod) and attribute is not BaseMod:
                        # 3. Instantiate the mod and save it
                        mod_instance = attribute()
                        cls.active_mods.append(mod_instance)
                        print(f"Loaded Mod: {mod_instance.name} v{mod_instance.version} by {mod_instance.author}")

    @classmethod
    def trigger_engine_init(cls, settings, cache):
        for mod in cls.active_mods:
            mod.on_engine_init(settings, cache)

    @classmethod
    def trigger_level_start(cls, world, spatial_grid):
        for mod in cls.active_mods:
            mod.on_level_start(world, spatial_grid)