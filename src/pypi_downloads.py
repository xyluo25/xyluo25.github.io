# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, April 24th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


def pypi_downloads(package_name: str) -> dict:
    """Get the total downloads of a package from PyPI.

    Args:
        package (str): The name of the package.

    Returns:
        dict: A dictionary containing the total downloads of the package.

    Examples:
        >>> pypi_downloads("pandas")
            2770112521
    """

    # import packages required for this function
    import requests
    import json

    # prepare the url and get the response
    url = 'https://api.pepy.tech/api/projects/' + package_name

    try:
        # get data from url
        response = requests.get(url)

        # convert the response to a dictionary
        content_dict = json.loads(response.content.decode("utf-8"))
        return content_dict["total_downloads"]
    except Exception:
        print(f"Error: {package_name} not found. returning 0 instead.")
        return 0


if __name__ == "__main__":
    package_list= ["exceltomysql", "exceltopostgresql", "exceltosqlserver",
                   "vissim2geojson", "DLSim", "pyhelpers", "osm2gmns", "plot4gmns"]

    download_list = [pypi_downloads(package_name) for package_name in package_list]
    print(download_list, sum(download_list))
