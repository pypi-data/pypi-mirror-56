import argparse
from . import *

parser = argparse.ArgumentParser(
    description='giqra, a library management program')
parser.add_argument('-p', '--profile', default='default',
    help='profile to open. each profile has its own database and preferences. the default profile is named `default`')
parser.add_argument('-d', '--directory', default=None,
    help='root config dir where profiles exist. defaults to a directory named `iqra` in the usual configuration path in the system (in linux, that would be `~/.config/iqra`)')

ns = parser.parse_args()

init(config_dir=ns.directory, profile=ns.profile)

initialize_gui()

start_main()

giqra_thread.stop_all()

