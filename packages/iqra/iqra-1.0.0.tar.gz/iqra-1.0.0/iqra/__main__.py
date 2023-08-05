import iqra
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='iqra, a library management program')
    parser.add_argument('-c', '--commit', action='store_true', default=False,
        help='commit before exit. opposite of -nc')
    parser.add_argument('-nc', '--no-commit', action='store_false',
        dest='commit',
        help='do not commit before exit. opposite of -nc. default')
    parser.add_argument('-p', '--profile', default='default',
        help='profile to open. each profile has its own database and preferences. the default profile is named `default`')
    parser.add_argument('-d', '--directory', default=None,
        help='root config dir where profiles exist. defaults to a directory named `iqra` in the usual configuration path in the system (in linux, that would be `~/.config/iqra`)')
    parser.add_argument('command', nargs=argparse.REMAINDER,
        help='command to be executed')
    
    ns = parser.parse_args()
    
    iqra_util = iqra.IqraUtil(config_dir=ns.directory, profile=ns.profile)
    
    if ns.command:
        iqra.IqraCmd(util=iqra_util).execute_line(ns.command)
    else:
        while True:
            try:
                iqra.IqraCmd(util=iqra_util).cmdloop()
                break
            except KeyboardInterrupt:
                print()
    
    if ns.commit:
        print('commiting before exit')
        iqra_util.get_scoped_session().commit()

if __name__ == '__main__':
    main()

