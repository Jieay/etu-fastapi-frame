# -*- coding: utf-8 -*-
# @Time    : 2022/9/17 15:47
# @Author  : Jieay
# @File    : main.py
import os
import shutil
import sys
import uuid
from pathlib import Path
from . import __version__

BASE_DIR = Path(__file__).resolve().parent


class ManagementUtility:
    """
    Encapsulate the logic of the eff-admin utilities.
    """
    VERSION_LIST = ['0.95.2']
    SERVER_TYPE_LIST = ['cfg', 'ms']

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.version_list = self.VERSION_LIST
        self.cwd_dir = os.getcwd()
        self.data_root_dir = os.path.join(BASE_DIR, 'data')
        self.frame_root_dir = os.path.join(BASE_DIR, 'fastapi')
        self.server_type_list = self.SERVER_TYPE_LIST

    def main_help_text(self):
        """Return the script's main help text, as a string."""
        label_name = '\n'.join(['    {}'.format(x) for x in self.version_list])
        server_name = '\n'.join(['    {}'.format(x) for x in self.server_type_list])
        usage = [
            "",
            "usage: eff-admin label server project_name",
            "labels: ",
            label_name,
            "server: ",
            server_name,
        ]
        return '\n'.join(usage)

    def create_frame(self, label, server_type, project_name):
        """
        创建脚手架项目文件
        :param label: FastAPI版本
        :param server_type: 服务类型：cfg | ms
        :param project_name: 项目名称
        """
        if not os.path.exists(self.data_root_dir):
            os.makedirs(self.data_root_dir)
        tmp_data_dir = os.path.join(self.data_root_dir, uuid.uuid4().hex)
        frame_source_dir = os.path.join(self.frame_root_dir, label, server_type)
        # 创建临时文件
        if not os.path.exists(tmp_data_dir):
            shutil.copytree(
                src=frame_source_dir,
                dst=tmp_data_dir,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('__pycache__', '.git', '*.pyc', '.idea')
            )

        # 创建项目目录，生产脚手架稳文件
        create_project_dir = os.path.join(self.cwd_dir, project_name)
        if not os.path.exists(create_project_dir):
            shutil.copytree(tmp_data_dir, create_project_dir)

        # 删除临时文件
        if os.path.exists(tmp_data_dir):
            shutil.rmtree(tmp_data_dir)

        sys.stdout.write('Create scaffold finished.' + '\n')

    def execute(self):
        """
        Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropriate to that command, and run it.
        """
        sys.stdout.write('Welcome to EFF tools.' + '\n')
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        if subcommand in self.version_list:
            sys.stdout.write('Select the fastapi version: {}'.format(subcommand) + '\n')
            try:
                server_type = self.argv[2]
            except IndexError:
                server_type = None

            try:
                project_name = self.argv[3]
            except IndexError:
                project_name = None

            if server_type and project_name:
                if server_type in self.server_type_list:
                    sys.stdout.write('Select the fastapi server type: {}'.format(server_type) + '\n')
                    sys.stdout.write('Create project name: {}'.format(project_name) + '\n')
                    self.create_frame(label=subcommand, server_type=server_type, project_name=project_name)
                else:
                    sys.stdout.write(self.main_help_text() + '\n')
            else:
                sys.stdout.write(self.main_help_text() + '\n')

        elif subcommand == 'help':
            sys.stdout.write(self.main_help_text() + '\n')

        # Special-cases: We want 'eff-admin --version' and
        # 'eff-admin --help' to work, for backwards compatibility.
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write(__version__ + '\n')

        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            sys.stdout.write(self.main_help_text() + '\n')


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
