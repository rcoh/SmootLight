import cProfile
from LightInstallation import main
command = """main(['', 'config/Kuan.xml'])"""
cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
