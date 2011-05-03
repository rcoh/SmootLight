if __name__ == "__main__":
    import yappi
    from LightInstallation import main
    yappi.start()
    main(['','config/10kConfig.xml'])
    yappi.stop()
    yappi.print_stats()
