import dataclasses
import functools


class reify:
    def __init__(self, wrapped):
        self.wrapped = wrapped
        functools.update_wrapper(self, wrapped)

    def __get__(self, inst, cls=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def methdispatch(func):
    # https://stackoverflow.com/questions/24601722/how-can-i-use-functools-singledispatch-with-instance-methods
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


class adict(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self


class ConvertingDataclass:
    def __post_init__(self):
        for field in dataclasses.fields(self):
            try:
                converter = field.metadata["converter"]
            except KeyError:
                pass
            else:
                setattr(self, field.name, converter(getattr(self, field.name)))


def linear_gradient(start, end, n=10):
    """
    https://bsou.io/posts/color-gradients-with-python
    """
    steps = [start]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = tuple(
            int(start[j] + (float(t) / (n - 1)) * (end[j] - start[j]))
            for j in range(len(start))
        )
        # Add it to our list of output colors
        steps.append(curr_vector)

    return steps


def color_to_hex(color):
    return "".join(f"{a:02X}" for a in color)
