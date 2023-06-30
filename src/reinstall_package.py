# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, June 29th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

def reinstall_package(pkg_lst: list) -> None:
    """Reinstall the package.

    Args:
        pkg_lst (list): A list of package names.
    """
    import subprocess
    import sys

    for pkg in pkg_lst:
        status = subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall"] + [pkg])
        if status == 0:
            print(f"    : {pkg} has been reinstalled successfully.")
        else:
            print(f"    : {pkg} has been reinstalled failed.")


if __name__ == "__main__":

    plst = ["utdf2gmns", "exceltopostgresql", "exceltomysql", "exceltosqlserver", "vissim2geojson"]

    reinstall_package(plst)
