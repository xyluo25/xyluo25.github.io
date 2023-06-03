# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, February 20th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import re
import os
import urllib.request
import json
import sys


class GitHubFileDownloader:
    def __init__(self, repo_url, flatten_files=True, output_dir="./"):
        """The GitHubFileDownloader is used to Downloads the files and directories in repo_url.

        Args:
            repo_url (str): The URL of the GitHub repository to download from. Can be a blob or tree path.
                directory: "https://github.com/xyluo25/openNetwork/blob/main/docs"
                single file: "https://github.com/xyluo25/openNetwork/blob/main/docs/canada_cities.csv"
            flatten_files (bool, optional): If flatten is specified, the contents of any and all sub-directories
                                            will be pulled upwards into the root folder. Defaults to True.
            output_dir (str, optional): The output directory to write. Defaults to "./".
        """

        self.repo_url = repo_url
        self.flatten = flatten_files
        self.output_dir = output_dir

    def create_url(self, url):  # sourcery skip: use-getitem-for-re-match-groups
        """
        From the given url, produce a URL that is compatible with Github's REST API. Can handle blob or tree paths.
        """
        repo_only_url = re.compile(
            r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$")
        re_branch = re.compile("/(tree|blob)/(.+?)/")

        # Check if the given url is a url to a GitHub repo. If it is, tell the
        # user to use 'git clone' to download it
        if re.match(repo_only_url, url):
            print(
                "✘ The given url is a complete repository. Use 'git clone' to download the repository")
            sys.exit()

        # extract the branch name from the given url (e.g master)
        branch = re_branch.search(url)
        download_dirs = url[branch.end():]
        api_url = (url[:branch.start()].replace("github.com", "api.github.com/repos",
                   1) + "/contents/" + download_dirs + "?ref=" + branch.group(2))
        return api_url, download_dirs

    def download(self):
        # generate the url which returns the JSON data
        api_url, download_dirs = self.create_url(self.repo_url)

        # To handle file names.
        if self.flatten:
            dir_out = self.output_dir
        elif len(download_dirs.split(".")) == 0:
            dir_out = os.path.join(self.output_dir, download_dirs)
        else:
            dir_out = os.path.join(
                self.output_dir, "/".join(download_dirs.split("/")[:-1]))

        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            response = urllib.request.urlretrieve(api_url)
        except KeyboardInterrupt:
            # when CTRL+C is pressed during the execution of this script,
            # bring the cursor to the beginning, erase the current line, and dont make a new line
            print("✘ Got interrupted")
            sys.exit()

        if not self.flatten:
            # make a directory with the name which is taken from
            # the actual repo
            os.makedirs(dir_out, exist_ok=True)

        # total files count
        total_files = 0

        with open(response[0], "r") as f:
            data = json.load(f)
            # getting the total number of files so that we
            # can use it for the output information later
            total_files += len(data)

            print("Total files: ", data)

            # If the data is a file, download it as one.
            if isinstance(data, dict) and data["type"] == "file":
                try:
                    # download the file
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(
                        data["download_url"], os.path.join(dir_out, data["name"]))
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    print("Downloaded: " + "{}".format(data["name"]))

                    return total_files
                except KeyboardInterrupt:
                    # when CTRL+C is pressed during the execution of this script,
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    print("✘ Got interrupted")
                    sys.exit()

            for file in data:
                file_url = file["download_url"]
                file_path = file["path"]
                path = os.path.basename(file_path) if self.flatten else file_path
                dirname = os.path.dirname(path)

                if dirname != '':
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                if file_url is not None:
                    file_name = file["name"]

                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)
                        # download the file
                        urllib.request.urlretrieve(file_url, path)

                        # bring the cursor to the beginning, erase the current line, and dont make a new line
                        print(f"Downloaded: {file_name}")

                    except KeyboardInterrupt:
                        # when CTRL+C is pressed during the execution of this script,
                        # bring the cursor to the beginning, erase the current line, and dont make a new line
                        print("✘ Got interrupted")
                        sys.exit()
                else:
                    self.download(file["html_url"], self.flatten, download_dirs)

        return total_files


if __name__ == "__main__":
    # Example
    url = r"https://github.com/xyluo25/OSM2GMNS/tree/master/sample%20networks/Dubai"
    url = r"https://github.com/xyluo25/openNetwork/blob/main/docs/canada_cities.csv"

    downloader = GitHubFileDownloader(url)
    downloader.download()
