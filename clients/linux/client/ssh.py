import sys


class ManualParserDecorator:
    def __init__(self, parser, server: str, server_port: int, username: str, ssuttle_method: str = "nft", verbose=False, **kwargs):
        self.parser = parser
        self.server = server
        self.server_port = server_port
        self.username = username
        self.sshuttle_method = ssuttle_method
        self.verbose = verbose

    def parse_args(self, args=None, namespace=None):
        args = [
            '--dns',
            '-r',
            f'{self.username}@{self.server}:{self.server_port}',
            '0.0.0.0/0',
            '--method',
            f'{self.sshuttle_method}',
            '--no-latency-control',
        ]
        if self.verbose:
            args.append("-v")
        output = self.parser.parse_args(args)
        return output

    def error(self, message):
        self.parser.error(message)


class DirectParserDecorator:
    def __init__(self, parser):
        self.parser = parser

    def parse_args(self, args=None, namespace=None):
        output = self.parser.parse_args(args=args)
        return output

    def error(self, message):
        self.parser.error(message)


class SShuttleController:

    def __init__(
            self,
            server: str,
            server_port: int,
            username: str,
            verbose: bool = False,
    ):
        self.server = server
        self.server_port = server_port
        self.username = username
        self.verbose = verbose

    def start(self):
        """
        Create a monkey patch for parser from
        https://github.com/sshuttle/sshuttle/blob/faf34e14e0904ffecbd3082d7fd41689ea7d1f6a/sshuttle/options.py#L174

        The new class should override `parse` method and call super with passed arguments to hit the cpython at:
        https://github.com/python/cpython/blob/53d9cd95cd91f1a291a3923acb95e0e86942291a/Lib/argparse.py#L1861

        """
        # Patching parser
        from sshuttle import options
        options.parser = ManualParserDecorator(
            options.parser,
            self.server,
            self.server_port,
            self.username,
            verbose=self.verbose
        )

        from sshuttle.cmdline import main
        main()

    def sshuttle_args(self):
        from sshuttle import options
        options.parser = DirectParserDecorator(options.parser)

        from sshuttle.cmdline import main
        sys.exit(main())
