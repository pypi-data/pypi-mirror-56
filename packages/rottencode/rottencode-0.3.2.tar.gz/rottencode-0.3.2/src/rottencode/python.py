import pathlib
import typing

from . import utils

PACKAGE_FILE_NAME = "__init__.py"


# XXX we need this extra class since singledispatch is not able to infer the
# type lazily
class NameBase:
    __slots__ = ("parts",)

    @utils.methdispatch
    def __init__(self, name):
        self.parts: typing.Tuple[str, ...] = tuple()


class Name(NameBase):
    """A dotted python name.

    Either a module or an attribute of a module.
    """

    @NameBase.__init__.register
    def _init_name(self, name: NameBase):
        self.parts = name.parts

    @NameBase.__init__.register
    def _init_tuple(self, parts: tuple):
        self.parts = parts

    @NameBase.__init__.register
    def _init_str(self, name: str):
        self.parts = tuple(name.split("."))

    def __getitem__(self, index):
        return self.parts[index]

    def __hash__(self):
        return hash(self.parts)

    def __eq__(self, other: typing.Union[object, str, typing.Tuple[str, ...], "Name"]):
        if isinstance(other, Name):
            return self.parts == other.parts
        if isinstance(other, tuple):
            return self.parts == other
        if isinstance(other, str):
            return self.parts == tuple(other.split("."))
        return False

    def __lt__(self, other):
        if isinstance(other, Name):
            return self.parts < other.parts
        if isinstance(other, tuple):
            return self.parts < other
        if isinstance(other, str):
            return self.parts < tuple(other.split("."))
        return False

    def __iter__(self):
        return iter(self.parts)

    @property
    def parent(self):
        parent = self.__class__(self.parts[:-1])
        return parent

    @property
    def root(self):
        root = self.__class__(self.parts[0])
        return root

    def __truediv__(self, other):
        if isinstance(other, Name):
            extra_name = other.parts
        elif isinstance(other, tuple):
            extra_name = other
        elif isinstance(other, str):
            extra_name = tuple(other.split("."))
        else:
            raise ValueError(f"Cannot create Name from `{other}`", other)

        return self.__class__(self.parts + extra_name)

    def __str__(self):
        return ".".join(self.parts)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    @classmethod
    def from_relative_path(cls, path):
        is_package = path.name == PACKAGE_FILE_NAME
        name = cls((path.parent if is_package else path.with_name(path.stem)).parts)
        return name


class Module(Name):
    def __init__(self, name, path=None):
        super().__init__(name)
        self.path = pathlib.Path(path) if path else path

    @utils.reify
    def is_package(self):
        return self.path.name == PACKAGE_FILE_NAME or self.path.is_dir()

    @utils.reify
    def package_dir(self):
        if self.path.is_dir():
            return self.path
        return self.path.parent


class ExternalModule(Module):
    ...
