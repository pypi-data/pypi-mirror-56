"""Provides the World class."""

import re

from inspect import signature, _empty

from attr import attrs, attrib, Factory


__all__ = [
    'Trigger',
    'World',
    'DontAbortException',
    'dont_abort'
]


class DontAbortException(Exception):
    """Raised by dont_abort."""
    pass


def dont_abort():
    """Use this function to continue searching for triggers. Simply raises
    AbortException."""
    raise DontAbortException()


@attrs
class Trigger:
    """A trigger instance."""

    regexp = attrib()
    func = attrib()
    classes = attrib(default=Factory(tuple))
    priority = attrib(default=Factory(int))
    kwarg_names = attrib(default=Factory(list), init=False)

    def __attrs_post_init__(self):
        """Build the kwargs list."""
        for p in signature(self.func).parameters.values():
            if p.default is not _empty:
                self.kwarg_names.append(p.name)


@attrs
class World:
    """
    Instances of this object hold Trigger instances and a list of active
    classes.

    Use the trigger decorator to add new triggers.
    Override build_args to provide a callable which will return a 2-element
    tuple of (args, kwargs) which will be sent to your functions. This callable
    should expect the trigger which was matched, the regexp match as returned
    by trigger.regexp.match, then any arguments and keyword arguments passed to
    handle_line as arguments.
    Use enable_class and disable_class to enable or disable a class
    respectively.
    Override the is_active method to configure whether or not triggers are
    active.
    Override the sort_key method to configure how active triggers are sorted.
    Use the handle_line method to handle an incoming line.
    """

    trigger_class = attrib(default=Factory(lambda: Trigger))
    classes = attrib(default=Factory(list), init=False)
    active_triggers = attrib(default=Factory(list), init=False)
    inactive_triggers = attrib(default=Factory(list), init=False)

    def trigger(self, pattern, **kwargs):
        """A decorator to add triggers. The only required argument is pattern
        which will be converted to a regular expression. Any extra keyword
        arguments are passed to the class constructor. The decorated function
        will be passed arguments according to build_args."""
        regexp = re.compile(pattern)

        def inner(func):
            """Actually perform the add."""
            t = self.trigger_class(regexp, func, **kwargs)
            if self.is_active(t):
                self.active_triggers.append(t)
            else:
                self.inactive_triggers.append(t)
            return t
        return inner

    def is_active(self, trigger):
        """Returns True or False depending on whether a trigger is active or
        not. To do this trigger.classes is compared against self.classes. By
        default, a trigger with no classes is always considered active."""
        if not trigger.classes:
            return True
        return bool(
            [
                c for c in trigger.classes if c in self.classes
            ]
        )

    def build_args(self, trigger, match, *args, **kwargs):
        """Generate the positional and keyword arguments for passing to
        functions. Returns a 2-element tuple of (args, kwargs). Uses a trigger
        function's keyword arguments to ascertain which values to extract from
        kwargs."""
        _args = (*match.groups(), *args)
        _kwargs = match.groupdict().copy()
        for position, name in enumerate(trigger.kwarg_names):
            if name not in _kwargs:
                try:
                    _kwargs[name] = kwargs[name]
                except KeyError:
                    if len(_args) < position:
                        raise RuntimeError(
                            'No argument named %s was provided for trigger %r.'
                            % trigger
                        )
        return (_args, _kwargs)

    def sorted_key(self, trigger):
        """By default returns trigger.priority."""
        return trigger.priority

    def activate_trigger(self, trigger):
        """Activate a trigger, moving it from inactive_triggers to
        active_triggers."""
        self.inactive_triggers.remove(trigger)
        self.active_triggers.append(trigger)

    def activate_triggers(self, triggers):
        """Activate 0 or more triggers."""
        for trigger in triggers:
            self.activate_trigger(trigger)

    def deactivate_trigger(self, trigger):
        """Deactivate a trigger, moving it from active_triggers to
        inactive_triggers."""
        self.active_triggers.remove(trigger)
        self.inactive_triggers.append(trigger)

    def deactivate_triggers(self, triggers):
        """Deactivate 0 or more triggers."""
        for trigger in triggers:
            self.deactivate_trigger(trigger)

    def enable_classes(self, *classes):
        """Enable 0 or more classes, automatically activating and
        deactivating triggers."""
        self.classes.extend(classes)
        triggers = []  # Store them so the list doesn't change size.
        for trigger in self.inactive_triggers:
            if self.is_active(trigger):
                triggers.append(trigger)
        self.activate_triggers(triggers)

    def disable_classes(self, *classes):
        """Disable 0 or more classes, automatically activating and deactivating
        triggers."""
        self.classes = [c for c in self.classes if c not in classes]
        triggers = []  # Keep them so the list doesn't change size.
        for trigger in self.active_triggers:
            if not self.is_active(trigger):
                triggers.append(trigger)
        self.deactivate_triggers(triggers)

    def handle_line(self, line, *args, **kwargs):
        """Check the line for triggers and run the appropriate functions. Any
        matched triggers will have their functions called with the groups and
        named groups from the regular expression as arguments unless the
        build_args decorator has been used.
        Returns the number of matched triggers."""
        matched = 0
        for trigger in sorted(
            self.active_triggers,
            key=self.sorted_key
        ):
            m = trigger.regexp.match(line)
            if m:
                positional, named = self.build_args(
                    trigger, m, *args, **kwargs
                )
                matched += 1
                try:
                    trigger.func(*positional, **named)
                    break
                except DontAbortException:
                    continue
        return matched
