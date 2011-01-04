import cProfile
from LightInstallation import main
command = """main(['', 'config/Outdoor.xml'])"""
cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
