
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..ext.tracking import tracking, initialize, test_sentry
from ..ext.monitor import Monitor
from ..ext.config_cmd import config
import os

VERSION_BANNER = """
ML & data helper code! %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'ML & data helper code!'

        # text displayed at the bottom of --help output
        epilog = 'Usage: dt command [args] [kwargs]'

        # controller level arguments. ex: 'dt --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

        # arguments=[
        #     ### add a sample foo option under subcommand namespace
        #     ( [ '-f', '--foo' ],
        #       { 'help' : 'notorious foo option',
        #         'action'  : 'store',
        #         'dest' : 'foo' } ),
        # self.app.render(data, 'command1.jinja2')

    @ex(
        help='Monitor (lack of) GPU activity. Remeber to add & at the end',
        arguments=[
            (['-freq'],{
                "help" : "Second frequency between checks",
                "action" : "store"
            }),
            (['-n'], {
                "help" : "Number of checks before alert",
                "action" : "store"
            })
        ]
    )
    def monitor(self):
        delay = self.app.pargs.freq or 10
        alert_threshold = self.app.pargs.freq or 60

        monitor = Monitor(int(delay), int(alert_threshold))
        print(f'Monitor is running with d={delay} and thershold={alert_threshold}')


    # number of files
    @ex(
        help='Displays the number of files',
        arguments=[
            (['-d'], { 
            "help" : "which directory to show",
            "action" : "store" } ) 
        ]
    )
    def nf(self):
        loc = self.app.pargs.d or '.'
        os.system(f'ls {loc} | wc -l')


    @ex(
        help='Operations with config.',
        # TODO: currently both are required.
        arguments = [
            (['action'], {
                "help" : "One of {show, set, loc} \
                Show configs: Sentry DNS etc. \
                Set: Resets the config from CLI. \
                Shows the location of the config",
                'action' : "store",
            })
        ]
    )
    def config(self):
        args = self.app.pargs

        # shows config
        if args.action=='show':
            for attr in dir(config):
                if not attr.startswith('_'):
                    print(f"{attr}: {getattr(config,attr)}")

        # shows the path of the config
        if args.action=='loc':
            print(os.path.abspath(__file__))

        # resets the config 
        # TODO this config method needs programmatic acces for spot instances
        if args.action=='set':
            initialize(overwrite=True)


    @ex(
        help='Tracks your ML code till finish',
        arguments=[
            (['flags'], {
                'help' : 'Which flags you want to pass to the underlying script.'
                         'e.g. --parallel --batch_size 256',
                'action' : "store"
            }),
            (['-ns'], {    
                'help' : 'Shuts down the computer between in the shutdown_hours.'
                        'Set to 22-08. Default: True',
                "action" : 'store'
            }),
            (['-t'], {
                'help' : 'If we are testing / doing a dry run. Default: False',
                "action" : "store"
            }),
            (['-cfg'],{
                'help': "location of the config file",
                "action" : "store",
            }),
            (['-p'],{
                "help": "which Python interpreter to use."
                        " Default is determined by `which python3`",
                "action" : "store"
            })
        ]
    )

    def track(self):
        ''' 'Tracks experiments by making a Sentry alert when a script finishes. ''' 
        args = self.app.pargs
        if self.app.pargs is not None:
            tracking(args.flags, args.t, args.ns, args.p)

    @ex(
        help='Test if sentry DSN is set up correctly.'
    )
    def test(self):
        test_sentry()