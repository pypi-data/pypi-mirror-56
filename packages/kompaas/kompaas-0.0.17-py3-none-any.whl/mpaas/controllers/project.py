"""
Module that handles projects\n
A project serves as a scope to store one or multiple charts together.\n

Supports:\n
- Creating\n
- Using\n
- Getting\n
- Deleting
"""

import subprocess
import os
import shutil
from cement import Controller, ex
from ..mpaas_exceptions import ProjectExistsError, EmptyDirectoryError,\
    MissingProjectError, RenderError, NoContextError, DeployError,\
    NoConfigError, MissingRancherConfigError


class Project(Controller):
    """
    Child class of the Controller class.
    Handles the 'project' sub-commands.
    """
    class Meta:
        """
        Meta class attributes.
        'project' is a nested sub-command of the base 'mpaas' command
        """
        label = 'project'
        aliases = ['projects']
        stacked_type = 'nested'
        stacked_on = 'base'
        help = 'Handle projects.'

    @ex(
        help='Create a project',
        arguments=[
            (['project_name'],
             {'help': 'New file name',
              'action': 'store'}),

            (['-u'],
             {'help': "Do not set new project as current context",
              'action': 'store_false',
              'dest': 'use'})
        ],
    )
    def create(self):
        """
        Method that creates a new project.
        Requires a name.
        """
        project_name = str(self.app.pargs.project_name)

        project_location = self.app.config.get('mpaas', 'projects_path') + project_name

        #Check if project already exists
        if os.path.isdir(project_location):
            raise ProjectExistsError(project_name)
        else:
            #create a helm chart in projects directory
            os.makedirs(project_location)
            subprocess.run(['helm', 'create', project_location])
            #remove default templates to have a clean empty project
            shutil.rmtree(project_location + '/templates')
            os.remove(project_location + '/values.yaml')
            os.mkdir(project_location + '/templates')

            self.app.log.info('Created directory %s in %s' % (project_name, project_location))

            if self.app.pargs.use:
                self.app.ch.set_context_project(project_name)
                self.app.ch.set_context_chart('None')
                self.app.log.info('Set current context to %s' % (project_name))

    @ex(
        help="Enter a project's context.",
        arguments=[
            (['project_name'],
             {'help': 'Target project name',
              'action': 'store'})
        ],
    )
    def use(self):
        """
        Method to set current context to target project.
        """
        current_project = str(self.app.pargs.project_name)
        projects_path = self.app.config.get('mpaas', 'projects_path')

        #Check if target project exists
        if os.path.isdir(projects_path + current_project):
            self.app.ch.set_context_project(current_project)
            self.app.ch.set_context_chart('None')
            self.app.log.info('Using context %s' % (current_project))
        else:
            raise MissingProjectError(current_project)

    @ex(
        help='List all existing projects',
    )
    def get(self):
        """
        Lists current projects from the projects directory.
        Renders output using a jinja2 template.
        """
        projects_path = self.app.config.get('mpaas', 'projects_path')

        if os.path.isdir(projects_path) is not True:
            os.makedirs(projects_path)

        if not os.listdir(projects_path):
            raise EmptyDirectoryError('Projects')

        else:
            projects = os.listdir(projects_path)
            data = {'names': [], 'context': self.app.ch.get_context_all()}

            for project in projects:
                data['names'].append(str(project))

            self.app.render(data, 'list/projects.jinja2')

    @ex(
        help='Create a project',
        arguments=[
            (['project_name'],
             {'help': 'New file name',
              'action': 'store'})
        ],
    )
    def delete(self):
        """
        Deletes target project.
        Sets current context to none if the context
        was set to deleted project.
        """
        project_name = self.app.pargs.project_name
        projects_path = self.app.config.get('mpaas', 'projects_path')
        project_path = projects_path + project_name

        #Check if project exists
        if os.path.isdir(project_path):
            shutil.rmtree(project_path)
            self.app.log.info('Successfully deleted project %s.' % (project_name))
            if project_name == self.app.ch.get_context_project():
                self.app.ch.set_context_project('None')
                self.app.ch.set_context_chart('None')
                self.app.log.info('Switched context to None')
        else:
            raise MissingProjectError(project_name)

    @ex(
        help="Render current project's yaml file",
    )
    def render(self):
        """
        Outputs the yaml representation of current project using helm.
        """

        project_name = self.app.ch.get_context_project()
        project_location = self.app.config.get('mpaas', 'projects_path') + project_name

        if project_name != 'None':
            try:
                subprocess.run(['helm', 'template', project_location, '-n', project_name])
            except:
                raise RenderError(project_name)
        else:
            raise NoContextError()

    @ex(
        help='List all existing projects',
        arguments=[

            (['-n', '--namespace'],
             {'action': 'store',
              'dest': 'namespace'}),

            (['--dryrun'],
             {'action': 'store_true'}),

            (['--rancher'],
             {'action': 'store_true'})

        ]
    )
    def deploy(self):
        """
        Deploys current project using kubectl.
        You can choose destination namespace using -n .
        You can perform a dry-run by using --dryrun
        """

        if not self.app.config_handler.check_config() and not self.app.pargs.rancher:
            raise NoConfigError()

        project_name = self.app.ch.get_context_project()
        if project_name != 'None':

            project_path = self.app.ch.getcontext_path()

            if not self.app.pargs.rancher:
                args = ['kubectl', 'apply', '-f',
                        project_path + '/temp.yaml']
            else:
                args = ['rancher', 'kubectl', 'apply', '-f',
                        project_path + '/temp.yaml']

            if self.app.pargs.dryrun:
                args.extend(['--dry-run'])

            #Output yaml representation of current helm chart to temp file
            with open(project_path + '/temp.yaml', 'w+') as resource_file:
                try:
                    #add namspace to relase rendering if present
                    if self.app.pargs.namespace:
                        temp = subprocess.check_output(['helm', 'template',
                                                        project_path,
                                                        '-n', project_name,
                                                        '--namespace', self.app.pargs.namespace])
                    else:
                        temp = subprocess.check_output(['helm', 'template',
                                                        project_path, '-n', project_name])
                    temp = temp.decode("utf-8")
                    resource_file.write(temp)
                except:
                    raise RenderError(project_name)

            #Deploy using kubernetes apply and temp file
            if not self.app.pargs.namespace:
                try:
                    print(subprocess.check_output(args).decode("utf-8"))
                except:
                    if subprocess.call(['rancher',
                                        'context',
                                        'current'], stdout=open(os.devnull, 'wb')):
                        if self.app.pargs.rancher:
                            raise MissingRancherConfigError
                    raise DeployError(project_name)

            #If namespace argument provided, deploy to that namespace instead
            else:
                try:
                    args.extend(['-n', self.app.pargs.namespace])
                    print(subprocess.check_output(args).decode("utf-8"))
                except:
                    if subprocess.call(['rancher',
                                        'context',
                                        'current'], stdout=open(os.devnull, 'wb')):
                        if self.app.pargs.rancher:
                            raise MissingRancherConfigError
                    raise DeployError(project_name)

        else:
            raise NoContextError()
