from Misc.Mods_Manager import BaseMod

class SpeedMod(BaseMod):
    """  # Buffs the player speed """
    name = "Speed Demon"
    author = "Xavier"

    def on_engine_init(self, settings, cache):
        original_speed = settings.GAME.PLAYER_SPEED
        settings.GAME.PLAYER_SPEED = original_speed 
        
        print(f"[{self.name}] loaded! Player speed increased from {original_speed} to {settings.GAME.PLAYER_SPEED}")