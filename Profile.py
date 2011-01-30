import cProfile
from LightInstallation import main
command = """main(['', 'config/6thFloorOSC.xml'])"""
cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
