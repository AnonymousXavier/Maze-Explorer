class BaseMod:
    """Every custom mod MUST inherit from this class."""
    name = "Unknown Mod"
    author = "Unknown"
    version = "1.0"

    def on_engine_init(self, settings, cache):
        """Fires once when the game boots. Great for tweaking global rules or loading custom sprites."""
        pass

    def on_level_start(self, world, spatial_grid):
        """Fires when the maze finishes generating. Great for spawning custom entities."""
        pass

    def on_update(self, world, spatial_grid, events, dt):
        """Fires every single frame. Great for custom logic and overriding components."""
        pass