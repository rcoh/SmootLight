import cProfile
from LightInstallation import main
command = """main(['', 'config/FireflyDemo.xml'])"""
cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
