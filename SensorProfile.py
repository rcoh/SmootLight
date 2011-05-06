if __name__ == "__main__":
    import yappi
    from LightInstallation import main
    yappi.start()
    main(['','config/SensorTest.xml'])
    yappi.stop()
    yappi.print_stats()
