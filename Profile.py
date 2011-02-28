if __name__ == "__main__":
    import cProfile
    from LightInstallation import main
    command = """main(['', 'config/Demo.xml'])"""
    cProfile.runctx(command, globals(), locals(), filename="smootlight.profile")
