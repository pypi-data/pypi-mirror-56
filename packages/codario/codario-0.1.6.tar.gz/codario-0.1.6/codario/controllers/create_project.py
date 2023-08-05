from cement import Controller, ex, shell
import urllib3, json, getpass, re, os

class CreateProject(Controller):
    class Meta:
        label = 'create-project'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='Create a project using interactive mode.',
        arguments=[
            ([ '--key' ], { 'help' : 'The API Key.', 'action' : 'store', 'dest' : 'key' }),
        ]
    )
    def create_project(self):
        if self.app.pargs.key is None:
            if os.getenv('CODARIO_API_KEY', None) is not None:
                self.app.pargs.key = os.getenv('CODARIO_API_KEY')
            else:
                self.app.log.error('The argument "--key" is required.')
                return

        '''Get name'''
        p = shell.Prompt('>> Name:', default=None)
        name = p.prompt()

        http = urllib3.PoolManager()

        '''Get repositories'''
        r = http.request(
            'GET',
            self.app.base_url + '/repositories',
            headers={'Content-Type': 'application/json', 'X-API-KEY': self.app.pargs.key}
        )

        data = r.data.decode('utf-8')
        response = json.loads(data)

        if response.get('repos'):
            repos = response['repos']
        else:
            self.app.log.error(response['message'][0])
            return

        '''Get repository url'''
        if repos:
            reposKeys = list(repos.keys())
            reposKeys.insert(0, 'custom')

            print()
            p = shell.Prompt('>> Choose the source of repository:',
                options=reposKeys,
                numbered = True,
            )

            if 'custom' == p.prompt():
                p = shell.Prompt('Git path:', default=None)
                git_path = p.prompt()
            else:
                options = []

                git_provider_name = p.prompt()

                for repo in repos[git_provider_name]['list']:
                    options.append(repo['name'])

                print()
                p = shell.Prompt('>> Choose the source of repository:',
                    options=options,
                    numbered = True,
                )

                for repo in repos[git_provider_name]['list']:
                    if repo['name'] == p.prompt():
                        git_path = repo['ssh']
                        git_provider = {
                            'provider': git_provider_name,
                            'id': repo['id'],
                        }
        else:
            p = shell.Prompt('Git path:', default=None)
            git_path = p.prompt()
            git_provider = []

        '''Get branches'''
        fields = {
            'action': 'get_branches',
            'repository': git_path,
        }

        r = http.request(
            'GET',
            self.app.base_url + '/repository',
            headers={'Content-Type': 'application/json', 'X-API-KEY': self.app.pargs.key},
            fields=fields
        )

        data = r.data.decode('utf-8')
        response = json.loads(data)

        if response.get('success') and response['success'] is True:
            branches = response['data']['branches']
        else:
            self.app.log.error(response['message'][0])
            return

        print()
        p = shell.Prompt('>> Choose the main branch:',
            options=branches,
            numbered = True,
        )

        main_branch = p.prompt()

        '''Get project types'''
        fields = {
            'action': 'get_all_available_types_of_projects',
            'repository': git_path,
            'branch': main_branch,
        }

        r = http.request(
            'GET',
            self.app.base_url + '/repository',
            headers={'Content-Type': 'application/json', 'X-API-KEY': self.app.pargs.key},
            fields=fields
        )

        data = r.data.decode('utf-8')
        response = json.loads(data)

        if response.get('success') and response['success'] is True:
            options = []

            for option in response['data']['options']:
                options.append('folder: ' + option['root_folder'] + ' (' + option['manager_label'] + ')')

            options.append('choose a project manager and root folder manually')
        else:
            self.app.log.error(response['message'][0])
            return

        print()
        p = shell.Prompt('>> Choose the project to monitoring:',
            options=options,
            numbered = True,
        )

        project_type = p.prompt()

        if 'choose a project manager and root folder manually' == project_type:
            print()
            p = shell.Prompt('>> Root folder:', default=None)
            root_folder = p.prompt()
            print()
            p = shell.Prompt('>> Manager:', default=None)
            manager = p.prompt()
        else:
            for option in response['data']['options']:
                prepared = 'folder: ' + option['root_folder'] + ' (' + option['manager_label'] + ')'

                if prepared == project_type:
                    root_folder = option['root_folder']
                    manager = option['manager']

        '''Predefined configs'''
        print()
        p = shell.Prompt('>> Do you want to use predefined configs?',
            options=['yes', 'no'],
        )

        if 'yes' == p.prompt():
            r = http.request(
                'GET',
                self.app.base_url + '/integrations',
                headers={'Content-Type': 'application/json', 'X-API-KEY': self.app.pargs.key},
                fields=fields
            )

            data = r.data.decode('utf-8')
            response = json.loads(data)

            patterns = [
                '^.+?@(.+?):',
                'https://(?:.+?@)?(.+?)/.+?\.git',
            ]

            suited_integration = None

            for pattern in patterns:
                match = re.search(pattern, git_path)

                if match:
                    for service in response['services']:
                        if 'git_provider' == service['type'] and service['parameters']['host'][8:] == match.group(1):
                            suited_integration = service['alias']

            options = ['merge branch']

            if suited_integration is not None:
                options.append('pull request')

            print()
            p = shell.Prompt('>> Choose the way to delivery updates:',
                options=options,
                numbered = True,
            )

            if 'merge branch' == p.prompt():
                predefined_configs = 'mb'
                extra = {}
            else:
                predefined_configs = 'pl'
                extra = {'git-provider': suited_integration}

            print()
            p = shell.Prompt('>> Choose how do you want to get info about updates:',
                options=['no inform', 'inform via email'],
                numbered = True,
            )

            if 'inform via email' == p.prompt():
                predefined_configs = predefined_configs + '-with-emails'
        else:
            predefined_configs = 'empty'
            extra = {}

        '''Create a project'''
        body = {
            'name': name,
            'manager': manager,
            'git_path': git_path,
            'main_branch': main_branch,
            'root_folder': root_folder,
            'configs': predefined_configs,
            'git_provider': git_provider,
            'extra': extra,
        }

        r = http.request(
            'POST',
            self.app.base_url + '/project',
            headers={'Content-Type': 'application/json', 'X-API-KEY': self.app.pargs.key},
            body=json.dumps(body).encode('utf-8')
        )

        data = r.data.decode('utf-8')
        response = json.loads(data)

        print()

        if response.get('success') and response['success'] is True:
            self.app.log.info(response['message'][0])
        else:
            self.app.log.error(response['message'][0])
