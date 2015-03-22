from siteman import Site, Server
import argparse

def main_func():
    parser = argparse.ArgumentParser(description='Create lighttpd configuration files and fcgi.py files.')

    parser.add_argument('--config', "-c", type=argparse.FileType('r'), nargs=1,
                        required=True,
                        help='site list file')
    parser.add_argument('--print', "-p", action='store_true',
                        required=False,
                        help='print all file data to console')
    parser.add_argument('--dry_run', action='store_true',
                        required=False,
                        help='just print file actions')

    args = vars(parser.parse_args())
    config_file = args['config'][0]
    dry_run = args.get('dry_run', False)
    server = Server(config_file, dry_run=dry_run)
    if not args['print']:
        server.write()
    else:
        for site in server.sites:
            print "------------------------------------------------"
            print "fcgi.py"
            print "------------------------------------------------"
            print site.generate_fcgi_file()
            print "------------------------------------------------"
            print "lighttpd.conf"
            print "------------------------------------------------"
            print site.generate_lighttpd_config()

if __name__ == "__main__":
    main_func()
