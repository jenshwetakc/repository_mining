from pydriller import Repository
import json
import re
import time
import javalang

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
# LIMIT = 20
start = time.time()
is_repo_loaded = True
tests_of_commits = []
total_commits = 0


for commit in Repository(REPO_URL).traverse_commits():
    total_commits += 1

    if is_repo_loaded:
        repo_load_time = time.time() - start
        print(f"load time {repo_load_time}")
        is_repo_loaded = False

    is_test_file = None

    # Loop through each files in a commit
    for file in commit.modified_files:
        is_test_file = (
            None
            if file.new_path is None
            else re.search(file_path_pattern, file.new_path)
        )
        if is_test_file:
            list_of_test_classes = []
            list_of_test_methods = []
            source_code = file.source_code
            # use library to parse
            # extract method_name and class_name
            try:
                tree = javalang.parse.parse(source_code)
                # Check if junit is imported

                is_junit_imported = False
                for import_name in tree.imports:
                    if "junit" in import_name.path:
                        is_junit_imported = True
                        break

                if is_junit_imported:
                    for test_class in tree.types:
                        class_name = test_class.name
                        if re.search(test_class_name_convention, class_name):
                            if class_name not in list_of_test_classes:
                                list_of_test_classes.append(class_name)
                            for test_method in test_class.methods:
                                method_name = test_method.name
                                if re.search(test_method_name_convention, method_name):
                                    method = class_name + ":" + method_name
                                    list_of_test_methods.append(method)

                        if len(list_of_test_classes) > 0:
                            test_commit = {
                                "commit": commit.hash,
                                "num_of_test_classes": len(list_of_test_classes),
                                "num_of_test_methods": len(list_of_test_methods),
                                "list_of_test_classes": list_of_test_classes,
                                "list_of_test_methods": list_of_test_methods,
                            }
                            tests_of_commits.append(test_commit)
                            list_of_test_classes = []
                            list_of_test_methods = []
            except Exception as error:
                print(f"Parsing error for commit_id {commit.hash} due to {str(error)}")
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

with open("./repositoryOutput1.json", "w") as f:
    json.dump(out, f, indent=4)
