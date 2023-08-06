
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..ext.tracking import tracking, initialize, test_sentry
from ..ext.monitor import Monitor
from ..ext.config_cmd import config
from ..ext.fluidstack import avail_fl_nodes, show_running
from ..ext.aws_sg import get_sg, update_sg_to_ip
from ..ext.aws_ec2 import get_ec2
from ..ext.sshconf import read_ssh_config
from pprint import pprint as pp
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

    @ex(
        help='AWS Security Groups helper functions',
        arguments=[
            (['action'],{
                "help" : "One of {update, show}",
                "action": "store"
            }),
            (['-name'],{
                "help" : "Name of the SG to act on",
                "action": "store"
            }),
            (['-ip'],{
                "help" : "IP to add to security group",
                "action": "store"
            }),
            (['-profile'],{
                "help" : "Which AWS profile should boto3 use",
                "action" : "store"
            })
        ]
    )
    def sg(self):
        if self.app.pargs.action=='show':
            pp(get_sg(self.app.pargs.name, self.app.pargs.profile))

        elif self.app.pargs.action=='update':
            update_sg_to_ip(sg_name=self.app.pargs.name, ip=self.app.pargs.ip,
                            profile=self.app.pargs.profile)

    @ex(
        help="AWS EC2 helper commands.",
        arguments=[
            (['action'],{
                    "help" : "To show one of {ls}.",
                    "action" : "store"
                }),
            (['-profile'],{
                "help" : "Which AWS profile should boto3 use.",
                "action": "store"
            })
        ]           
    )
    def ec2(self):
        if self.app.pargs.action=='ls':
            get_ec2('live', self.app.pargs.profile)

    @ex(
        help="Display all available Fluidstack nodes.",
        arguments=[
            (['action'],{
                "help" : "To show one of {avail, live}.",
                "action" : "store"
            }),
            (['-stats'],{
            "help" : "One of {all, gpus} to show either all (df) or gpus (json)",
            "action": "store"
            }),
            (['-n_gpu'],{
                "help" : "# of gpus required to be on the machine",
                "action" : "store"
            })
        ]
    )
    def fls(self):
        args = self.app.pargs
        if args.action=='avail':
            avail_fl_nodes(args.stats, args.n_gpu)
        elif args.action=='live':
            show_running()

        else:
            raise NotImplementedError('Set the first parg to one of {avail, live}')


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
        help="Copies things from zshrc.txt to ~/.bashrc or ~/zshrc",
        arguments = [
            (['shell'], {
                "help" : "One of {sh, zsh}. Imports a DT version of zshrc into bashrc or zshrc.",
                "action": "store"
            })
        ]
    )
    def load(self):
        zshrc = os.path.abspath(__file__).split('/')[:-2] + ['ext', 'zshrc.txt']
        zshrc_path = os.path.join('/'.join(zshrc)) 
        if self.app.pargs.shell == 'sh':
            os.system(f'cat {zshrc_path} >> ~/.bashrc ')
        if self.app.pargs.shell == 'zsh':
            os.system(f'cat {zshrc_path} >> ~/.zshrc ')
        else:
            raise NotImplementedError("Try one of {sh, zsh}")


    @ex(
        help='Operations on the SSH config',
        arguments=[
            (['action'],{
                "help" : "To show one of {set, ls, }.",
                "action" : "store"
            }),
            (['host'],{
            "help" : "Which SSH config host to change",
            "action": "store"
            }),
            (['-url'],{
                "help" : "The URL to update in the ssh config",
                "action" : "store"
            })
        ]
    )
    def ssh_conf():
        if self.app.pargs.action=='set':
            ssh_config_obj = read_ssh_config('/Users/jakub/.ssh/config')
            ssh_config_obj.set(self.app.pargs.host, self.app.pargs.url)
            ssh_config_obj.write('/Users/jakub/.ssh/config')
            print(ssh_config_obj.config())

        else:
            raise NotImplementedError()


    @ex(
        help='Operations with config.',
        arguments = [
            (['action'], {
                "help" : "One of {show, set, loc}: \
                *show*: show configs Sentry DNS etc. \
                *set*: Resets the config from CLI. \
                *loc*: shows the location of the config",
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

        else:
            raise NotImplementedError("Try one of {show, set, loc}")


    @ex(
        help='Tracks your ML code till finish',
        arguments=[
            (['flags'], {
                'help' : 'Which  script + flags you want to pass to the underlying python.'
                         'e.g. train.py --parallel --batch_size 256',
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