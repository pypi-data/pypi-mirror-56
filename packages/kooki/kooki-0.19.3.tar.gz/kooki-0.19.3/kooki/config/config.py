import os

import yaml

from kooki.tools import read_config_file

resource_dir_env = "KOOKI_DIR"
resource_dir_default = "~/.kooki"

jar_manager_env = "KOOKI_JAR_MANAGER"
jar_manager_default = [
    "https://gitlab.com/kooki/jar_manager/raw/master/jars.yml"
]

jar_config_file = "jar.yaml"


def get_kooki_dir():
    resource_dir = os.environ.get(resource_dir_env)
    if not resource_dir:
        resource_dir = os.path.expanduser(resource_dir_default)
    return resource_dir


def get_kooki_dir_jars():
    resources_dir = get_kooki_dir()
    jars_dir = os.path.join(resources_dir, "jars")
    return jars_dir


def get_kooki_jar_manager():
    jar_manager = os.environ.get(jar_manager_env)
    if jar_manager:
        jar_manager = yaml.safe_load(jar_manager)
    else:
        jar_manager = jar_manager_default
    return jar_manager


def get_kooki_jar_config(jar_name):
    user_jars_dir = get_kooki_dir_jars()
    jar_config_file_path = os.path.join(user_jars_dir, jar_name,
                                        jar_config_file)
    jar_config = read_config_file(jar_config_file_path, must_exist=False)
    return jar_config
