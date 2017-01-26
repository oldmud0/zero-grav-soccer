import glob, cx_Freeze

executables = [cx_Freeze.Executable("main.py", icon="res/icon.ico", targetName="zgsoccer.exe")]

cx_Freeze.setup(
        name="Zero-Gravity Soccer",
        options={"build_exe": {
            "optimize": 2,
#            "compressed": True,
            "include_msvcr": True,
            "packages":["pygame"]#,
            #"include_files": glob.glob("res/*.*")
            }
            },
        executables=executables)
            
