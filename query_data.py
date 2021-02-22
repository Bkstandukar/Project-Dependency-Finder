def query_string(repo_onwer, repo_name):
    body_param = '''
            {
            repository(owner: "%s", name: "%s") {
                description
                databaseId
                name
                owner {
                    login
                }
                releases(first: 3, orderBy: {field: CREATED_AT, direction: DESC}){
                    nodes{
                        tagName
                        name
                        author{
                            name
                        }
                        createdAt
                        publishedAt
                        updatedAt
                        isLatest
                        isPrerelease
                    }
                }
                primaryLanguage {
                    name
                }
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}){
                    nodes{
                        name
                    }
                }
                forkCount
                isFork
                parent{
                    name
                }
                licenseInfo{
                    name
                }
                dependencyGraphManifests(first: 50) {
                    nodes {
                        blobPath
                        parseable
                        dependenciesCount
                        dependencies {
                            nodes {
                            packageManager
                            packageName
                            repository {
                                databaseId
                                name
                                owner {
                                login
                                }
                                releases(first: 3, orderBy: {field: CREATED_AT, direction: DESC}){
                                    nodes{
                                        name
                                        author{
                                            name
                                        }
                                        createdAt
                                        publishedAt
                                        updatedAt
                                        isLatest
                                        isPrerelease
                                    }
                                }
                                primaryLanguage {
                                    name
                                }
                                languages(first: 10, orderBy: {field: SIZE, direction: DESC}){
                                    nodes{
                                        name
                                    }
                                }
                                forkCount
                                isFork
                                parent{
                                    name
                                }
                                licenseInfo{
                                    name
                                }
                            }
                            requirements
                            hasDependencies
                            }
                        }
                    }
                }
            }
        }
        '''

    query_data = (body_param % (repo_onwer, repo_name))
    return query_data
