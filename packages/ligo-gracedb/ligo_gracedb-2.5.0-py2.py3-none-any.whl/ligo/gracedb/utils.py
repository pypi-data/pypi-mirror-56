import os
import re
import six
import stat
from functools import wraps
from netrc import netrc, NetrcParseError
if os.name == 'posix':
    import pwd

EVENT_PREFIXES = ['G', 'E', 'H', 'M', 'T']
event_prefix_regex = re.compile(r'^({prefixes})\d+'.format(
    prefixes="|".join(EVENT_PREFIXES)))


# Decorator for class methods so that they work for events or superevents
def event_or_superevent(func):
    @wraps(func)
    def inner(self, object_id, *args, **kwargs):
        is_superevent = True
        if event_prefix_regex.match(object_id):
            is_superevent = False
        return func(self, object_id, is_superevent=is_superevent, *args,
                    **kwargs)
    return inner


# Function for checking arguments which can be strings or lists
# If a string, converts to list for ease of processing
def handle_str_or_list_arg(arg, arg_name):
    if arg:
        if isinstance(arg, six.string_types):
            arg = [arg]
        elif isinstance(arg, list):
            pass
        else:
            raise TypeError("{0} arg is {1}, should be str or list"
                            .format(arg_name, type(arg)))
    return arg


# Parse a datetime object out of the openssl output.
# Note that this returns a naive datetime object.
class safe_netrc(netrc):
    """The netrc.netrc class from the Python standard library applies access
    safety checks (requiring that the netrc file is readable only by the
    current user, and not by group members or other users) only if using the
    netrc file in the default location (~/.netrc). This subclass applies the
    same access safety checks regardless of the path to the netrc file."""

    def _parse(self, file, fp, *args, **kwargs):
        # Copied and adapted from netrc.py from Python 2.7
        if os.name == 'posix':
            prop = os.fstat(fp.fileno())
            if prop.st_uid != os.getuid():
                try:
                    fowner = pwd.getpwuid(prop.st_uid)[0]
                except KeyError:
                    fowner = 'uid %s' % prop.st_uid
                try:
                    user = pwd.getpwuid(os.getuid())[0]
                except KeyError:
                    user = 'uid %s' % os.getuid()
                raise NetrcParseError(
                    ("~/.netrc file owner (%s) does not match"
                     " current user (%s)") % (fowner, user),
                    file)
            if (prop.st_mode & (stat.S_IRWXG | stat.S_IRWXO)):
                raise NetrcParseError(
                    "~/.netrc access too permissive: access"
                    " permissions must restrict access to only"
                    " the owner", file)
        return netrc._parse(self, file, fp, *args, **kwargs)
