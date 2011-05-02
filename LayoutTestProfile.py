if __name__ == "__main__":
    import cProfile
    from LightInstallation import main
    command = """main(['', 'config/LayoutTest.xml'])"""
    cProfile.runctx(command, globals(), locals(), filename="layouttest.profile")
