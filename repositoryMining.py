from pydriller import Repository
import json
import re
import time

with open("input.json", "r") as file:
    url = json.load(file)
    REPO_URL = url["repo_url"]

out = {"location": "", "number_of_commits": 0, "tests_of_commits": []}
count = 1
LIMIT = 1000
pattern = r".test."

start = time.time()

is_repo_loaded = True

list_of_test_classes = []
list_of_test_methods = []
unique_test_classes = []
total_commits = []

for commit in Repository(REPO_URL).traverse_commits():
    if is_repo_loaded:
        repo_load_time = time.time() - start
        print(f"load time {repo_load_time}")
        is_repo_loaded = False

    is_test_file = None
    for file in commit.modified_files:
        is_test_file = (
            None if file.new_path is None else re.search(pattern, file.new_path)
        )
        if is_test_file:
            for method in file.changed_methods:
                class_and_method_name = method.name

                class_name = class_and_method_name.split("::")[0]

                list_of_test_classes.append(class_name)
                for unique_class_name in list_of_test_classes:
                    if unique_class_name not in unique_test_classes:
                        unique_test_classes.append(unique_class_name)
                list_of_test_methods.append(class_and_method_name)

    if is_test_file:
        test_commit = {
            "commit": commit.hash,
            "num_of_test_classes": len(list_of_test_classes),
            "num_of_test_methods": len(list_of_test_methods),
            "list_of_test_classes": unique_test_classes,
            "list_of_test_methods": list_of_test_methods,
        }
        total_commits.append(commit.hash)
        out["location"] = commit.project_path
        out["tests_of_commits"].append(test_commit)
        out["number_of_commits"] = len(total_commits)

        if count > LIMIT:
            break

    count += 1

end = time.time()
total_time = end - start
time_to_process_commit = total_time - repo_load_time
print(time_to_process_commit)

with open("./repositoryOutput.json", "w") as f:
    json.dump(out, f, indent=4)
