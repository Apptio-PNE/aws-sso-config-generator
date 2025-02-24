import argparse
import os

from aws_sso_config_generator.client import AwsSsoClient
from aws_sso_config_generator.config import ConfigWriter


def main():
    config = _parse_config()

    client = AwsSsoClient(region=config.region, start_url=config.start_url)
    writer = ConfigWriter(sso_start_url=config.start_url, sso_region=config.sso_region, region=config.region,
                          output=config.output, aws_vault=config.aws_vault)

    accounts = client.list_accounts()
    for account in sorted(accounts, key=lambda a: a.account_name):
        roles = client.list_account_roles(account.account_id)
        for role in sorted(roles, key=lambda r: r.role_name):
            writer.write_profile(account, role)


def _parse_config():
    parser = argparse.ArgumentParser(description='Generate AWS SSO named profiles for ~/.aws/config')
    parser.add_argument('--region', metavar='REGION', help='AWS region for generated profiles', default="us-west-2")
    parser.add_argument('--sso-region', metavar='REGION', help='AWS SSO region', default="us-west-2")
    parser.add_argument('--start-url', metavar='URL', help='AWS SSO start url', default="https://apptio-sso.awsapps.com/start")
    parser.add_argument('--output', help='output format for generated profiles', default="json")
    parser.add_argument('--aws-vault', help='injects custom credential process for aws-vault', action='store_const', const=True, default=True)
    args = parser.parse_args()

    return args
