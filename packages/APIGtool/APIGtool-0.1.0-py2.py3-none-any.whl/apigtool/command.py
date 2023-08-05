import sys
import logging
import click
import platform
from apigtool.utility import work_on_apigs
from apigtool.utility import list_apigs

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S'
)

valid_systems = [
    'linux',
    'darwin'
]


@click.group()
@click.version_option(version='0.1.0')
def cli():
    pass


@cli.command()
@click.option('--apig', '-a', help='APIG of interest', required=True)
@click.option('--stage', '-s', help='APIG stage of interest', required=True)
@click.option('--profile', '-p', help='credential profile')
@click.option('--region', '-r', help='AWS region')
@click.option('--on', '-o', help='on: true | false')
def log(apig, stage, profile, region, on):
    '''
    Work on logging for an APIG
    '''
    work_on_apigs(
        apig=apig,
        stage=stage,
        profile=profile,
        region=region,
        on=on
    )


@cli.command()
@click.option('--profile', '-p', help='credential profile')
@click.option('--region', '-r', help='AWS region')
def list(profile, region):
    '''
    Work on listing the API's
    '''
    list_apigs(
        profile=profile,
        region=region
    )


def verify_real_system():
    try:
        current_system = platform.system().lower()
        return current_system in valid_systems
    except:
        return False

if not verify_real_system():
    print('error: unsupported system')
    sys.exit(1)
