from cx_Freeze import Executable, setup

version = "1.0.0-alpha"

setup(
    name="CIMS-BOT",
    version=version,
    description="Cloud Infrastructure Management System Bot",
    executables=[Executable("main.py")],
)
