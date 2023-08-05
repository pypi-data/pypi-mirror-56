#


"""
Core functionalities
"""


import subprocess
import venv


class _EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """ Overrride """
        self.context = context
        self._upgrade()

    def _upgrade(self):
        requirements = ['pip', 'setuptools', 'wheel']
        command = [
            self.context.env_exe,
            '-m', 'pip',
            'install',
            '--upgrade',
        ]
        command.extend(requirements)
        subprocess.run(command, check=True)


def _venv_create(venv_dir):
    venv_builder = _EnvBuilder(with_pip=True)
    venv_builder.create(venv_dir)


def main(target_path):
    """ Main routine
    """
    _venv_create(target_path)


# EOF
