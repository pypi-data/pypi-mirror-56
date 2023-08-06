import json
import os

import re
import shutil

import sh
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Make a source distribution of the codebase.'

    def add_arguments(self, parser):
        parser.add_argument('--keep-old-static', dest='keep_old_static',
                            required=False, action='store_true', default=False,
                            help='Keep old production release static files.')
        parser.add_argument('--dirty-node-modules', dest='dirty_node_modules',
                            required=False, action='store_true', default=False,
                            help='Do not use the --yarn-clean-node-modules argument for ievv buildstatic. '
                                 'Normally not recommended, but useful if you know you have clean node '
                                 'modules with no symlinked packages or other things that may '
                                 'mess up the release.')
        parser.add_argument('--ignore-uncommitted-changes', dest='check_for_uncommitted_changes',
                            required=False, action='store_false', default=True,
                            help='Do not abort if we have uncommitted changes. Mostly only useful when '
                                 'developing this management command.')
        parser.add_argument('--patch', dest='patch',
                            required=False, action='store_true', default=False,
                            help='Patch version, use patch ONLY IF the release contains bug fixes.')
        parser.add_argument('--minor', dest='minor',
                            required=False, action='store_true', default=False,
                            help='Minor version, use minor when the release contains no breaking changes, '
                                 'new features and multiple bugfixes.')
        parser.add_argument('--major', dest='major',
                            required=False, action='store_true', default=False,
                            help='Major version, use major version if the release contains '
                                 'breaking changes and or major new features.')
        parser.add_argument('--no-confirm', dest='no_confirm',
                            required=False, action='store_true', default=False,
                            help='Release will pass all confirmation prompts. '
                                 'Only provide --no-confirm if you are not a humanoid such as a cat.')

    def __log_shell_command_stdout(self, line):
        """
        Called by :meth:`.run_shell_command` each time the shell
        command outputs anything to stdout.
        """
        self.stdout.write(line.rstrip())

    def __log_shell_command_stderr(self, line):
        """
        Called by :meth:`.run_shell_command` each time the shell
        command outputs anything to stderr.
        """
        self.stderr.write(line.rstrip())

    def __run_shell_command(self, executable, args=None, kwargs=None):
        """
        Run a shell command.

        Parameters:
            executable: The name or path of the executable.
            args: List of arguments for the ``sh.Command`` object.
            kwargs: Dict of keyword arguments for the ``sh.Command`` object.

        Raises:
            ShellCommandError: When the command fails. See :class:`.ShellCommandError`.
        """
        command = sh.Command(executable)
        args = args or []
        kwargs = kwargs or {}
        command(*args,
                _out=self.__log_shell_command_stdout,
                _err=self.__log_shell_command_stderr,
                **kwargs)

    def __validate_version_option(self, options):
        self.patch = options['patch']
        self.minor = options['minor']
        self.major = options['major']

        if ((self.patch and self.minor)
                or (self.minor and self.major)
                or (self.major and self.patch)
                or (self.patch and self.major and self.minor))\
                or (not self.patch and not self.major and not self.minor):
            raise CommandError(
                'Please provide only one semver option --patch, --minor or --major'
            )

    def get_version_json_file_path(self):
        try:
            return getattr(settings, 'IEVV_PROJECT_VERSIONJSON_PATH')
        except AttributeError:
            raise CommandError('The IEVV_PROJECT_VERSIONJSON_PATH setting is missing.')

    def get_version_from_version_json(self):
        with open(self.get_version_json_file_path(), 'r') as f:
            version_json = f.read()
        return json.loads(version_json)

    def write_version_json(self, version):
        with open(self.get_version_json_file_path(), 'w') as f:
            f.write(json.dumps(version))
            f.close()

    def get_built_static_directories(self):
        static_directories = []
        for app in settings.IEVVTASKS_BUILDSTATIC_APPS.iterapps():
            if app.appname not in self.__get_ignored_apps():
                static_directory = os.path.join(
                    app.get_appfolder(),
                    'static',
                    app.appname,
                    self.release_version)
                if os.path.exists(static_directory):
                    static_directories.append(static_directory)
        return static_directories

    def get_old_release_version(self):
        if self.current_version.endswith('-dev'):
            return self.current_version.replace('-dev', '')
        raise CommandError(
            'Detecting versions for production releases only work '
            'if the version stored in {} is formatted "[major].[minor].[patch]-dev".'.format(
                self.get_version_json_file_path()))

    def get_splitted_version(self):
        if self.current_version.endswith('-dev'):
            splitted_version = self.current_version.replace('-dev', '').split('.')
            return [int(splitted_version[0]), int(splitted_version[1]), int(splitted_version[2])]
        raise CommandError(
            'Detecting versions for production releases only work '
            'if the version stored in {} is formatted "[major].[minor].[patch]-dev".'.format(
                self.get_version_json_file_path()))

    def make_release_version(self):
        [major, minor, patch] = self.get_splitted_version()
        version = ''

        if self.patch:
            version = '{}.{}.{}'.format(major, minor, patch + 1)
            self.confirm('Are you sure you want to release patch version ({} -> {})?'
                         '\nYou should only release a patch version if the release contains ONLY bug fixes\n'
                         .format(self.get_old_release_version(), version),
                         'release patch')
        if self.minor:
            version = '{}.{}.0'.format(major, minor + 1)
            self.confirm('Are you sure you want to release minor version ({} -> {})?'
                         .format(self.get_old_release_version(), version), 'yes')
        if self.major:
            version = '{}.0.0'.format(major + 1)
            self.confirm('Are you sure you want to release major version ({} -> {})?\n'
                         .format(self.get_old_release_version(), version),
                         'bump major version to {}'.format(version))
        return version


    # def get_release_version(self):
    #     major_version = self.get_release_major_version()
    #     return '{}.0.0'.format(major_version)

    def get_new_version_after_release(self):
        return '{}-dev'.format(self.release_version)

    def set_release_version(self):
        self.write_version_json(version=self.release_version)

    @property
    def ievv_buildstatic_args(self):
        args = ['buildstatic', '--production']
        if not self.dirty_node_modules:
            args.append('--yarn-clean-node-modules')
        return args

    @property
    def ievv_buildstatic_command_string(self):
        return 'ievv {}'.format(' '.join(self.ievv_buildstatic_args))

    def get_extra_git_add_paths(self):
        return getattr(settings, 'IEVVTASKS_MAKE_SOURCE_DIST_EXTRA_GIT_ADD_PATHS', [])

    def build_release(self):
        self.__run_shell_command('ievv', args=self.ievv_buildstatic_args)
        git_add_args = ['add']
        git_add_args.extend(self.get_built_static_directories())
        git_add_args.append(self.get_version_json_file_path())
        git_add_args.append(self.get_extra_git_add_paths())
        self.__run_shell_command('git', args=git_add_args)

    def commit_release(self):
        self.__run_shell_command('git', args=[
            'commit', '-m', 'Release version: {}'.format(self.release_version)
        ])

    def tag_release(self):
        self.__run_shell_command('git', args=[
            'tag', 'v{}'.format(self.release_version)
        ])

    def build_and_commit(self):
        self.set_release_version()
        self.build_release()
        self.commit_release()
        self.tag_release()

    def revert_version_change(self):
        version = self.get_new_version_after_release()
        self.write_version_json(version=version)
        self.__run_shell_command('git', args=['add', self.get_version_json_file_path()])
        self.__run_shell_command('git', args=[
            'commit', '-m', 'Set version to: {}'.format(version)
        ])

    def print_preview(self):
        action_list = []
        if not self.keep_old_static:
            paths_to_delete = self.__get_version_build_folders_to_delete()
            action_list.extend([
                'Will delete the following old release folders: \n   - {}'.format(
                    '\n   - '.join(paths_to_delete)
                )
            ])
        action_list.extend([
            'Change {} to {!r}'.format(self.get_version_json_file_path(),
                                       self.release_version),
            self.ievv_buildstatic_command_string,
            'Git commit the files built by buildstatic and tag the commit with v{}'.format(
                self.release_version),
            'python setup.py sdist'
            'Change {} to: {!r}'.format(self.get_version_json_file_path(),
                                        self.get_new_version_after_release()),
            'Git commit the version change.',
        ])
        for action in action_list:
            self.stdout.write('- {}'.format(action))

    def __get_cli_input(self):
        """
        Support python 2 raw input.
        """
        if sys.version_info.major == 2:  # pragma: no cover
            return raw_input
        else:  # pragma: no cover
            return input

    def confirm(self, message, confirm_text):
        cli_input = self.__get_cli_input()
        if self.no_confirm:
            return
        try:
            try:
                if cli_input('{} [type "{}" to confirm or hit enter to abort] '.format(message, confirm_text)) != confirm_text:
                    raise CommandError('Confirmation failed, abort!')
                return
            except KeyboardInterrupt:
                self.stderr.write('\n')
                raise CommandError('Confirmation failed, abort!')

        except KeyboardInterrupt:
            self.stdout.write('\n')
            return

    def confirm_procedure(self):
        self.stdout.write('Summary of actions to be performed:')
        self.print_preview()
        self.stdout.write('\n')
        self.stdout.write('Are you sure you want to to build a source dist?')
        confirm_text = 'yes'
        self.confirm('', confirm_text)

    def has_git_changes(self):
        return sh.Command('git')('diff-index', 'HEAD').strip() != ''

    def __get_ignored_apps(self):
        return getattr(settings, 'IEVVTASKS_MAKE_SOURCE_DIST_IGNORE_APPS', set())

    def __should_delete_old_build_version_folder(self, dir_name):
        """
        Returns `True` if the regex matches the directory name.

        If the setting ``IEVVTASKS_MAKE_SOURCE_DIST_PRODUCTION_BUILD_VERSION_FOLDER_REGEX`` does
        not exist, we assume all old build folder should be deleted.
        """
        build_version_folder_regex = getattr(
            settings, 'IEVVTASKS_MAKE_SOURCE_DIST_PRODUCTION_BUILD_VERSION_FOLDER_REGEX', r'^\d+-dev?$')
        if build_version_folder_regex:
            return re.match(build_version_folder_regex, dir_name)
        return False

    def __get_version_build_folders_to_delete(self):
        buildstatic_ignore_apps = self.__get_ignored_apps()
        delete_version_paths = []
        for app in settings.IEVVTASKS_BUILDSTATIC_APPS.iterapps():
            if app.appname in buildstatic_ignore_apps:
                continue
            static_directory = os.path.join(
                app.get_appfolder(),
                'static',
                app.appname)
            if not os.path.exists(static_directory):
                continue
            for dir_name in os.listdir(static_directory):
                if self.__should_delete_old_build_version_folder(dir_name=dir_name):
                    absolute_path = os.path.join(static_directory, dir_name)
                    if os.path.isdir(absolute_path):
                        delete_version_paths.append(absolute_path)
        return delete_version_paths

    def remove_old_static_builds(self):
        """
        Remove old production builds.
        """
        self.stdout.write('\nDeleting old production builds')
        for version_folder_path in self.__get_version_build_folders_to_delete():
            self.stdout.write(' -- Deleting: {}'.format(version_folder_path))
            git = sh.Command('git')
            try:
                git(['rm', '-r', version_folder_path])
            except sh.ErrorReturnCode:
                shutil.rmtree(version_folder_path)

    def make_source_dist(self):
        self.__run_shell_command(sys.executable, args=['setup.py', 'sdist'])

    def handle(self, *args, **options):
        check_for_uncommitted_changes = options['check_for_uncommitted_changes']
        self.keep_old_static = options['keep_old_static']
        self.dirty_node_modules = options['dirty_node_modules']
        self.no_confirm = options['no_confirm']
        self.__validate_version_option(options)
        self.current_version = None
        self.should_make_source_dist = True

        self.current_version = self.get_version_from_version_json()
        if check_for_uncommitted_changes and self.has_git_changes():
            raise CommandError('You have uncommitted changes. Aborting.')

        self.release_version = self.make_release_version()
        self.confirm_procedure()

        if not self.keep_old_static:
            self.remove_old_static_builds()

        self.current_version = self.get_version_from_version_json()
        self.build_and_commit()

        try:
            self.make_source_dist()
        finally:
            if not self.current_version:
                raise CommandError('Something is wrong - current_version is empty/blank/none')
            self.revert_version_change()
