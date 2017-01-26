import glob, cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
        name="Zero-Gravity Soccer",
        options={"build_exe": {
            "packages":["pygame"],
            "include_files": glob.glob("res/*.*")
            }
            },
        executables=executables)
            
