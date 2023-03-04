from cx_Freeze import setup, Executable

base = None    

executables = [Executable("uno_synth.py", base=base)]

packages = ["construct", "os", "argparse", "sys", "mido", "rtmidi"]
options = {
    'build_exe': {    
        'packages':packages,
        'excludes':["pygame", "numpy"],
    },    
}

setup(
    name = "uno_synth.py",
    options = options,
    version = "0.1.0.0",
    description = "Library for working with Uno Synth config files",
    executables = executables
)
