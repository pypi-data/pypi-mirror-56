import os
import random
import string
import tempfile
import textwrap
from functools import lru_cache

import empy
import pretty_output
from kooki.tools import get_front_matter, read_file

from .exception import ErrorEvaluatingExpression, MissingFile
from .jars import search_file, search_file_in_context
from .metadata import Metadata
from .renderer import KookiRenderer, render

PREFIX = "@"
MARKDOWN_EXT = ".md"


class Extension:

    level = 0

    def __init__(self, document, extension_path, content=None):
        if content is not None:
            file_content = content
        else:
            file_content = read_file(extension_path)

        _, self.file_extension = os.path.splitext(extension_path)
        self.extension_path = extension_path
        self.document = document
        self.front_matter, self.content = get_front_matter(file_content)

    def __call__(self, *args, **kwargs):

        try:
            metadata = self.parse_metadata(*args, **kwargs)
            content = self.content

            self.debug_tree_start()

            caller = Caller(
                self.document,
                self.extension_path,
                metadata=metadata,
                file_extension=self.file_extension,
            )
            content = self.apply_interpreter(content, caller, prefix=PREFIX)

            if self.file_extension == MARKDOWN_EXT:
                content = render(content, caller)

            interpreter = empy.Interpreter()
            interpreter.setPrefix("§")
            content = interpreter.expand(content, Caller.placeholders)

            self.debug_tree_stop()

            return content

        except ErrorEvaluatingExpression as e:
            e.add_path(self.extension_path)
            raise e

    def apply_interpreter(self, content, metadata, prefix):
        interpreter = empy.Interpreter()
        interpreter.setPrefix(prefix)
        result = interpreter.expand(content, metadata)
        return result

    def parse_metadata(self, *args, **kwargs):
        metadata = Metadata()
        metadata.update(self.front_matter)
        metadata.update(self.document.metadata)
        new_args = {}
        for index, arg in enumerate(args):
            new_args["arg{}".format(index)] = arg
        metadata.update(**new_args)
        metadata.update(**kwargs)
        return metadata

    def debug_tree_start(self):
        pretty_output.debug_on()
        if Extension.level == 0:
            pretty_output.colored(self.extension_path, "white", "on_yellow")
        else:
            message = ""
            for i in range(0, self.level - 1):
                message += "│   "
            message += "├"
            message += "─" * 2
            message += " "
            pretty_output.colored(message, "white", "on_yellow", end="")
            pretty_output.colored(self.extension_path, "white", "on_yellow")
        Extension.level += 1
        pretty_output.debug_off()

    def debug_tree_stop(self):
        Extension.level -= 1


def is_builtin_class_instance(obj):
    return obj.__class__.__module__ == "__builtin__"


class Caller:

    placeholders = {}
    tempary_extensions = []

    @classmethod
    def clean(cls):
        for tempary_extension in cls.tempary_extensions:
            os.unlink(tempary_extension.name)

    def __init__(self,
                 document,
                 extension_path,
                 metadata,
                 file_extension,
                 call_path=""):
        self.document = document
        self.extension_path = extension_path
        self.call_path = call_path
        self.metadata = metadata
        self.file_extension = file_extension

        self.kooki_embeded_functions = Metadata()
        self.kooki_embeded_functions["kooki"] = Metadata({
            "find":
            self.find,
            "load":
            self.load,
            "ext":
            self.ext,
            "get":
            self.get,
            "name":
            self.document.name,
            "toc":
            KookiRenderer.toc,
        })

        self.metadata.update({
            "find": self.find_deprecated,
            "load": self.load_deprecated,
            "ext": self.ext_deprecated,
            "get": self.get_deprecated,
        })

        self.metadata.update(self.kooki_embeded_functions)
        self.data = None

    def __getattr__(self, name):
        return self.get_item(name)

    def __getitem__(self, key):
        return self.get_item(key)

    def __setitem__(self, key, value):
        self.metadata[key] = value

    def get_item(self, key):

        if key == "locals":

            def call_locals():
                return locals()

            return call_locals

        if self.call_path != "":
            new_call_path = "{}/{}".format(self.call_path, key)
        else:
            new_call_path = key

        self.metadata.update(__builtins__)
        self.metadata.update(locals()["self"].metadata)
        value = self.metadata.get(key)

        if value is not None:
            if is_builtin_class_instance(value):
                return type("", (type(value), Caller), {})(
                    self.document,
                    self.extension_path,
                    self.metadata,
                    file_extension=self.file_extension,
                    call_path=new_call_path,
                )
            else:
                return value
        else:
            return Caller(
                self.document,
                self.extension_path,
                self.metadata,
                file_extension=self.file_extension,
                call_path=new_call_path,
            )

    def __repr__(self):
        return ""

    def __call__(self, *args, placeholder=True, **kwargs):

        path = search_file_in_context(self.document, self.extension_path,
                                      self.call_path)
        if not path:
            path = search_file(self.document, self.call_path)

        if not path:
            raise Exception("cannot find {}".format(self.call_path))

        if os.path.isdir(path):
            full_path_md = os.path.join(path, "__kooki__.md")
            full_path_spec = os.path.join(
                path, "__kooki__{}".format(self.file_extension))
            if os.path.isfile(full_path_md):
                full_path = full_path_md
            elif os.path.isfile(full_path_spec):
                full_path = full_path_spec
            else:
                raise Exception(
                    textwrap.dedent("""\
                    You try to call this extension: {}
                    Cannot find one of those files in the directory.
                    - {}
                    - {}
                    """.format(path, full_path_md, full_path_spec)))
        else:
            full_path = path

        extension = self.create_extension(full_path)
        result = extension(*args, **kwargs)
        if placeholder:
            name = self.get_var_name()
            Caller.placeholders[name] = result
            return "§({})".format(name)
        else:
            return result

    def deprecation_message(self, message):
        pretty_output.warning(
            textwrap.dedent("""\
            Warning: {}
            {}
        """.format(self.extension_path, message)))

    @lru_cache(maxsize=256)
    def create_extension(self, full_path):
        extension = Extension(self.document, full_path)
        return extension

    def find_deprecated(self, file_path):
        self.deprecation_message(
            """'find' alone is deprecated, use 'kooki.find' instead.""")
        return self.find(file_path)

    def find(self, file_path):
        file_full_path = search_file(self.document, file_path)
        if file_full_path:
            return file_full_path
        else:
            raise MissingFile(self.document.jars, file_path)

    def ext_deprecated(self, path, *args, **kwargs):
        self.deprecation_message(
            """'ext' alone is deprecated, use 'kooki.ext' instead""")
        return self.ext(path, *args, **kwargs)

    def ext(self, path, *args, **kwargs):
        path = os.path.join(os.getcwd(), path)
        pretty_output.info(path)
        if os.path.isdir(path):
            full_path_md = os.path.join(path, "__kooki__.md")
            full_path_spec = os.path.join(
                path, "__kooki__{}".format(self.file_extension))
            if os.path.isfile(full_path_md):
                full_path = full_path_md
            elif os.path.isfile(full_path_spec):
                full_path = full_path_spec
            else:
                raise Exception(
                    textwrap.dedent("""\
                    You try to call this extension: {}
                    Cannot find one of those files in the directory.
                    - {}
                    - {}
                    """.format(path, full_path_md, full_path_spec)))
        else:
            full_path = path

        extension = self.create_extension(full_path)
        result = extension(*args, **kwargs)
        name = self.get_var_name()
        Caller.placeholders[name] = result
        return "§({})".format(name)

    def load_deprecated(self, content, template_extension):
        self.deprecation_message(
            """'load' alone is deprecated, use 'kooki.load' instead""")
        return self.load(content, template_extension)

    def load(self, content, template_extension):
        directory_path = os.path.dirname(self.extension_path)
        temp_extension = tempfile.NamedTemporaryFile(
            suffix=template_extension, dir=directory_path, delete=False)
        temp_extension.write(bytes(content, "utf-8"))
        temp_extension.close()
        Caller.tempary_extensions.append(temp_extension)
        return Extension(self.document, temp_extension.name)

    def get_deprecated(self, key, default=""):
        self.deprecation_message(
            """'get' alone is deprecated, use 'kooki.get' instead""")
        return self.get(key, default)

    def get(self, key, default=""):
        if key in self.metadata:
            return self.metadata[key]
        else:
            return default

    def get_var_name(self):
        name = "".join(
            random.choice(string.ascii_uppercase) for _ in range(25))
        while name in Caller.placeholders:
            name = "".join(
                random.choice(string.ascii_uppercase) for _ in range(25))
        return name
