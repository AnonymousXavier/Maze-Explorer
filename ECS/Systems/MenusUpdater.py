from ECS.Systems import ClickingSystem, HoveringSystem

def process(ui: dict):
	HoveringSystem.process(ui)
	ClickingSystem.process(ui)