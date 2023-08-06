# let's do a splash screen when our module is imported and initialized
# feel free to change this
splash = True

module_name = "Junkyard"
__version__ = "0.0.3a2"

# if not main file
if __name__ != "__main__":
    # print a version of the
    if splash:
        print(f"Powered by {module_name} ({__version__})")
