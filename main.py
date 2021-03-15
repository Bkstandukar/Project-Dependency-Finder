from query_data import query_string
import requests
import pandas as pd
import time
import json
import os
import argparse

parent_flag = True

level = []
data_table = []
time_str_file = time.strftime("%m-%d-%Y_%H-%M-%S")


def get_token_key():
    with open("cred.json", "r") as cred:
        token_json = json.load(cred)
        token_map = token_json["token_key"]
        return token_map


def get_test_data(token, repo_owner, repo_name, parent="root", depth=1):
    data = query_string(f"{repo_owner}", f"{repo_name}")
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.hawkgirl-preview+json"
    }
    get_info = requests.post(url=url, json={'query': data}, headers=headers, verify=True)
    query_result = get_info.json()
    global level

    for node_repo in query_result['data']['repository']['dependencyGraphManifests']['nodes']:
        for node_package in node_repo['dependencies']['nodes']:
            node_package["From"] = parent
            try:
                print(f"DataBaseID: {node_package['repository']['databaseId']} ---> From: {parent}")
            except TypeError:
                pass
            else:
                data_table.append(node_package)
                level.append(node_package)
                if (depth == 0 or len(level) < depth) and node_package['hasDependencies'] and node_package[
                    'repository']:
                    # prevent from getting same databaseID in a loop
                    if node_package['repository']['databaseId'] not in level:
                        time.sleep(0.5)
                        owner_info = node_package['repository']['owner']['login']
                        repo_name_info = node_package['repository']['name']
                        yield from get_test_data(token_key, owner_info, repo_name_info,
                                                 parent=node_package["repository"]["databaseId"])
                level.pop()


def get_file_name(file_name, directory_name=None):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    filename = f"{directory_name}\{file_name}_{time_str_file}.csv"
    return filename


if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="Find project dependencies using GitHub's API v4")
    argp.add_argument('repository', help='Input repository name as foo/bar')
    argp.add_argument('--depth', type=int, default=1, help='Depth to search')
    args = argp.parse_args()

    repo_info = args.repository.split('/')
    if len(repo_info) != 2:
        argp.error("Input repository name as Bkstandukar/ProjectDependency")
    repo_onwer_details, repo_name_detail = repo_info

    token_key = get_token_key()
    try:
        all_data = [x for x in get_test_data(token_key, repo_onwer_details, repo_name_detail, depth=args.depth)]
    except TypeError:
        print("i have an error")

    repo_dependencies_df = pd.json_normalize(data_table, max_level=500)
    print(repo_dependencies_df)
    file_to_save = get_file_name(f"{repo_onwer_details}_{repo_name_detail}", directory_name="query_results")
    repo_dependencies_df.to_csv(file_to_save, index=False)

    print(f"file is saved as: {file_to_save}")