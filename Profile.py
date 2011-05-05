if __name__ == "__main__":
    import cProfile
    from LightInstallation import main

    command = """main(['', 'config/RoughGum.xml'])"""

    cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
