# Import Hooks -> Added to sys.meta_path automatically
import textwrap
import sys
from .imports import *
from .urlimport import install_path_hook, remove_path_hook
install_path_hook()

# Network tools
from .net.sslsocket import ServerSocket
from .net.server_factory import ServerFactory
from.net.evloop import EventLoop
from .net.sslsocket import ClientSocket, UPiServerSocket, UPiClientSocket
from .net.sslsocket import (hostname, decode, encode, loads, dumps)
from .net.mail import send_mail, compose_mail

# SQl console utils
from .cli.sql import (SqlPrompt, prompt, get_sql_keywords, Input, HandleSQLResults)

# Utils
from .utils import IniParser, read_ini

# Win32 API, requires pywin32
import sys
if sys.platform == 'win32':
    from .win32.utils import get_idle_duration, SingleInstance

# Handling dates and timezones
from .dates import current_date, current_datetime, current_time
from .dates import local_timezone, convert_timezone, mktimezone
from .dates import strftime, strptime, patch_datetime

# Decorators
from .decorators import timer, time_codeblock, multimethod


# import module objects
from . import dates
from . import decorators
from . import imports
from . import utils
from . import cli
from . import net

if sys.platform == 'win32':
    from . import win32
