if __name__ == "__main__":
    import yappi
    from LightInstallation import main
    yappi.start()
    main(['','config/sensors/pedFollowing/1ColorTrail.xml'])
    yappi.stop()
    yappi.print_stats()
