import cProfile
from LightInstallation import main
command = """main(['', 'config/6thFloor.xml'])"""
cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
