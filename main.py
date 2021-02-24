from pprint import pprint
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

    for m in query_result['data']['repository']['dependencyGraphManifests']['nodes']:
        for dep in m['dependencies']['nodes']:
            dep["From"] = parent
            try:
                # since dep['repository'] can be none
                print(f"DataBaseID: {dep['repository']['databaseId']} ---> From: {parent}")
            except TypeError:
                pass
            else:
                # if dep not in data_table:
                data_table.append(dep)
                level.append(dep)
                if (depth == 0 or len(level) < depth) and dep['hasDependencies'] and dep['repository']:
                    # prevent from getting same databaseID in a loop
                    if dep['repository']['databaseId'] not in level:
                        time.sleep(0.2)
                        owner_info = dep['repository']['owner']['login']
                        repo_name_info = dep['repository']['name']
                        yield from get_test_data(token_key, owner_info, repo_name_info,
                                                 parent=dep["repository"]["databaseId"])
                level.pop()


def get_file_name(file_name, directory_name=None):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    filename = f"{directory_name}\{file_name}_{time_str_file}.csv"
    return filename


if __name__ == '__main__':
    argp = argparse.ArgumentParser(description="Find project dependencies using GitHub's API")
    argp.add_argument('repository', help='Input repository name as Bkstandukar/ProjectDependency')
    argp.add_argument('--depth', type=int, default=1, help='Depth to search')
    args = argp.parse_args()

    repo_info = args.repository.split('/')
    if len(repo_info) != 2:
        argp.error("Input repository name as Bkstandukar/ProjectDependency")
    repo_onwer_details, repo_name_detail = repo_info

    token_key = get_token_key()

    all_data = [x for x in get_test_data(token_key, repo_onwer_details, repo_name_detail, depth=2)]

    okay_df = pd.json_normalize(data_table, max_level=500)
    # okay_df = okay_df.drop()
    print(okay_df)
    file_to_save = get_file_name(f"{repo_onwer_details}_{repo_name_detail}", directory_name="query_results")
    okay_df.to_csv(file_to_save, index=False)

    print(f"file is save as: {file_to_save}")
