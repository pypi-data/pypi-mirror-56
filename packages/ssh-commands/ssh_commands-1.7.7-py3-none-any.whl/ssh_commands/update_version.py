from os import getenv
from ssh_commands.commands import replace_secret_vars_projects


class UpdateVersion:
    """
    Update version info.
    Arguments:
        variable_name(str) - Environment variable name
        increment(int) - Increment for version
        max_value(int) - max increment value
        gitlab_token(str) - Gitlab private token
    Properties:
        variable_name(str) - Environment variable name
        increment(int) - Increment for version
        max_value(int) - max increment value
        version(str) - Package version
        gitlab_token(str) - Gitlab private token
    """
    def __init__(
            self,
            variable_name,
            gitlab_token=None,
            increment=1,
            max_value=50
    ):
        self.variable_name = variable_name
        self.version = getenv(variable_name, "1.0.0")
        if len(self.version) == 0:
            raise AttributeError("Unknown version")

        self.version_parts = self.version.split(".")
        self.max_value = int(max_value)
        self.increment = int(increment)
        self.gitlab_token = gitlab_token

    def get_version(self):
        """
        Get next version.

        :return: str
        """
        v = self.version_parts
        v.reverse()
        ret_objects = list(v)

        for index, part in enumerate(v):
            next_part = int(part) + 1
            index_check = index + 1

            if next_part >= self.max_value and index != len(v) - 1:
                if index != len(v) - 1:
                    ret_objects[index_check] = "0" if index_check != len(v) - 1 else str(next_part + 1)
                    ret_objects[index] = "0"
                continue

            ret_objects[index] = str(next_part)

            break

        ret_objects.reverse()

        return ".".join(ret_objects)

    def save_new_version(self, version=None, projects=None):
        """
        Save new version in gitlab.

        :param version: Version value. Default is None
        :type version: str|None
        :param projects: Projects list.
        :type projects: list|none

        :return:
        """
        version = version if version is not None else self.version
        replace_secret_vars_projects(
            {
                self.variable_name: [self.variable_name]
            }, {
                self.variable_name: version
            },
            projects
        )
