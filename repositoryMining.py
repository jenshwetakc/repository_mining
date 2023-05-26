from pydriller import Repository, Git
from pydriller.git import Git
import json
import re
import time
import javalang
import os
import platform

import shutil


# Take input
with open("input.json", "r") as file:
    url = json.load(file)
    REPO_URL = url["repo_url"]

out = {"location": "", "number_of_commits": 0, "tests_of_commits": []}

# Regex for validation
file_path_pattern = r".test."
test_class_name_convention = r"\b\w+[tT]est\b"
test_method_name_convention = r"\btest\w*_?\w+"


# for testing
# count = 1
# LIMIT = 100
start = time.time()
is_repo_loaded = True

tests_of_commits = []
total_commits = 0

# to Identify the directory and pass project_directory accordingly

operationg_system = platform.system()
if operationg_system == "Windows":
    project_directory = os.getcwd() + "\\."
    project_directory = project_directory.replace("\\", "/")
else:
    project_directory = "."

reposiroty_name = REPO_URL.split("/")[-1].split(".")[0]
local_repository = None
commit_hash = []

for commit in Repository(REPO_URL, clone_repo_to=project_directory).traverse_commits():
    list_of_test_classes = []
    list_of_test_methods = []
    total_commits += 1

    if is_repo_loaded:
        repo_load_time = time.time() - start
        print(f"load time {repo_load_time}")
        local_repository = Git(reposiroty_name)
        is_repo_loaded = False

    is_test_file = None

    # Loop through each files in a commit
    local_repository.checkout(commit.hash)
    files_path = local_repository.files()

    for file_path in files_path:
        is_test_file = (
            None if file_path is None else re.search(file_path_pattern, file_path)
        )
        if is_test_file:
            # use library to parse, extract method_name and class_name
            try:
                file_data = open(file_path).read()
                tree = javalang.parse.parse(file_data)

                for test_class in tree.types:
                    class_name = test_class.name
                    package_name = tree.package.name
                if re.search(test_class_name_convention, class_name):
                    full_class_name = package_name + "." + class_name
                    for test_method in test_class.methods:
                        method_name = test_method.name
                        if re.search(test_method_name_convention, method_name):
                            if full_class_name not in list_of_test_classes:
                                list_of_test_classes.append(full_class_name)
                            method = full_class_name + ":" + method_name
                            list_of_test_methods.append(method)
            except Exception as error:
                print(f"Parsing error for commit_id {commit.hash} due to {str(error)}")
    if len(list_of_test_classes) > 0:
        test_commit = {
            "commit": commit.hash,
            "num_of_test_classes": len(list_of_test_classes),
            "num_of_test_methods": len(list_of_test_methods),
            "list_of_test_classes": list_of_test_classes,
            "list_of_test_methods": list_of_test_methods,
        }
        tests_of_commits.append(test_commit)

    # for testing
    # if count > LIMIT:
    #     break
    # count += 1

out["location"] = commit.project_path
out["tests_of_commits"] = tests_of_commits
out["number_of_commits"] = total_commits

end = time.time()
total_time = end - start
time_to_process_commit = total_time - repo_load_time
print("processing time : {}".format(time_to_process_commit))

with open("./repositoryOutput.json", "w") as f:
    json.dump(out, f, indent=4)

shutil.rmtree(reposiroty_name)
