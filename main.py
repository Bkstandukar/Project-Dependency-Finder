from pprint import pprint
from query_data import query_string
import requests
import pandas as pd
import json
import csv

parent_flag = True

level = []

data_table = []


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
            # json_obj = json.dumps(dep, indent=4)
            # print(json_obj)
            get_inside_out(dep, 'repository')
            data_table.append(dep)

            try:
                print(f"kaha bata aayeko timi: {dep['repository']['databaseId']} ---> {parent}")
            except TypeError:
                pass
            else:
                level.append(dep['repository']['databaseId'])
                if (depth == 0 or len(level) < depth) and dep['hasDependencies'] and dep['repository']:
                    if dep['repository']['databaseId'] not in level:
                        owner_info = dep['repository']['owner']['login']
                        repo_name_info = dep['repository']['name']
                        yield from get_test_data(token_key, owner_info, repo_name_info,
                                                 parent=dep["repository"]["databaseId"])
                level.pop()


def get_inside_out(table_name, column_name):
    for k, i in table_name[column_name].items():
        table_name[k] = i
        print(table_name)
    return table_name


token_key = "f75cec4db2826a45ba5d8c81bde707d8a63b3395"
repo_onwer_details = "chandip"
repo_name_detail = "django"

all_data = [x for x in get_test_data(token_key, repo_onwer_details, repo_name_detail, depth=1)]

okay_df = pd.DataFrame(data_table)
okay_df = okay_df.drop(columns=["repository"], axis=1)
print(okay_df)
okay_df.to_csv("test.csv", index=False)


