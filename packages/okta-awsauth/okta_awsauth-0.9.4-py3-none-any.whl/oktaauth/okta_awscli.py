""" Wrapper script for awscli which handles Okta auth """
# pylint: disable=C0325,R0913,R0914
import os
from sys import exit
from subprocess import call

import datetime
import pytz
import tzlocal
import fileinput
import re

import logging
import click
from version import __version__
from oktaauth.okta_auth import OktaAuth
from oktaauth.okta_auth_config import OktaAuthConfig
from oktaauth.aws_auth import AwsAuth

import re

def get_credentials(aws_auth, okta_profile, profile,
                    verbose, logger, totp_token, cache):
    """ Gets credentials from Okta """

    okta_auth_config = OktaAuthConfig(logger)
    okta = OktaAuth(okta_profile, verbose, logger, totp_token, okta_auth_config)

    _, assertion = okta.get_assertion()
    
    role = aws_auth.choose_aws_role(assertion)
    principal_arn, role_arn = role

    duration = okta_auth_config.duration_for(okta_profile)

    sts_token = aws_auth.get_sts_token(
        role_arn,
        principal_arn,
        assertion,
        duration=duration,
        logger=logger
    )
    access_key_id = sts_token['AccessKeyId']
    secret_access_key = sts_token['SecretAccessKey']
    session_token = sts_token['SessionToken']
    session_token_expiry = sts_token['Expiration']
    logger.info("Session token expires on: %s" % session_token_expiry)

    if not profile:
        exports = console_output(access_key_id, secret_access_key,
                                 session_token, verbose)
        if cache:
            cache = open("%s/.okta-credentials.cache" %
                         (os.path.expanduser('~'),), 'w')
            cache.write(exports)
            cache.close()
        exit(0)
    else:
        aws_auth.write_sts_token(profile, access_key_id,
                                 secret_access_key, session_token)

def get_cred(aws_auth, okta_profile,
                    verbose, logger, totp_token, cache):
    """ Gets Roles from Okta """

    okta_auth_config = OktaAuthConfig(logger)
    okta = OktaAuth(okta_profile, verbose, logger, totp_token, okta_auth_config)

    _, assertion = okta.get_assertion()
    
    role = aws_auth.list_roles(assertion)

    roles = []
    for r in range(len(role)):
        principal_arn, role_arn = role[r]
        roles.append(role_arn)

    f = open("%s/.okta-aws-roles" %
        (os.path.expanduser('~'),), 'w')
        
    for option in roles:
        f.write(option + "\r\n")

    return roles

def refresh_token(aws_auth, okta_profile, profile, verbose, logger, totp_token, cache, request, alias="NotSet"):
    """ Refresh aws token """
    okta_auth_config = OktaAuthConfig(logger)
    okta = OktaAuth(okta_profile, verbose, logger, totp_token, okta_auth_config)

    _, assertion = okta.get_assertion()
    
    role = aws_auth.update_role(assertion, request)
    principal_arn, role_arn = role

    duration = okta_auth_config.duration_for(okta_profile)

    sts_token = aws_auth.get_sts_token(
        role_arn,
        principal_arn,
        assertion,
        duration=duration,
        logger=logger
    )

    timenow = datetime.datetime.now()
    expires = sts_token['Expiration']

    format = "%Y-%m-%d %H:%M:%S.%f"

    left = expires.astimezone(pytz.utc)
    timenow = timenow.astimezone(pytz.utc)
    timeleft = left - timenow
    secondsLeft = int(timeleft.total_seconds())
    
    os.environ['OKTA'] = str(secondsLeft)

    file = "%s/.aws/credentials" % (os.path.expanduser('~'),)
    aliases = {}
    for line in fileinput.input([file], inplace=False):
        p = re.match("\[(.*?)\]", line)
        if p:
            al = p[1]
            aliases[al] = {}
        c = re.match("[ ]*([^ ]*)[ ]*=[ ]*([^ ]*)", line)
        if c:
            if "\n" in c[1]:
                name = c[1].rstrip("\n")
                credential_name = name
            else:
                credential_name = c[1]
            if "\n" in c[2]:
                key = c[2].rstrip("\n")
                credential_key = key
            else:
                credential_key = c[2]

            aliases[al][credential_name] = credential_key

    f = open("%s/.aws/credentials" %
        (os.path.expanduser('~'),), 'a+')

    if alias in aliases:
        if "default" in aliases:
            aliases["default"]["aws_access_key_id"] = aliases[alias]["aws_access_key_id"] 
            aliases["default"]["aws_secret_access_key"] = aliases[alias]["aws_secret_access_key"]
            aliases["default"]["aws_session_token"] = aliases[alias]["aws_session_token"]

            reWriteFile(aliases)
        else:
            writeDefault(sts_token)

    else:
        if alias != "NotSet":
            f.write(
                f'''\n[{alias}]
aws_access_key_id = {sts_token["AccessKeyId"]}
aws_secret_access_key = {sts_token["SecretAccessKey"]}
aws_session_token = {sts_token["SessionToken"]}\n'''
                )

            if "default" in aliases:
                aliases["default"]["aws_access_key_id"] = sts_token['AccessKeyId'] 
                aliases["default"]["aws_secret_access_key"] = sts_token['SecretAccessKey']
                aliases["default"]["aws_session_token"] = sts_token['SessionToken']

                reWriteFile(aliases)
            else:
                writeDefault(sts_token)

        else:
            if "default" in aliases:
                aliases["default"]["aws_access_key_id"] = sts_token['AccessKeyId']
                aliases["default"]["aws_secret_access_key"] = sts_token['SecretAccessKey']
                aliases["default"]["aws_session_token"] = sts_token['SessionToken']

                reWriteFile(aliases)
            else:
                writeDefault(sts_token)

def writeDefault(sts_token):
    f = open("%s/.aws/credentials" %
        (os.path.expanduser('~'),), 'a+')

    f.write(
        f'''\n[default]
aws_access_key_id = {sts_token["AccessKeyId"]}
aws_secret_access_key = {sts_token["SecretAccessKey"]}
aws_session_token = {sts_token["SessionToken"]}\n'''
        )

def reWriteFile(aliases):
    o = open("%s/.aws/credentials" %
        (os.path.expanduser('~'),), 'w')

    newFile = "# This File is managed by Okta-STS\n"
    for a in aliases:
        newFile += f'''\n[{a}]
aws_access_key_id = {aliases[a]["aws_access_key_id"]}\naws_secret_access_key = {aliases[a]["aws_secret_access_key"]}\naws_session_token = {aliases[a]["aws_session_token"]}\n'''

    o.write(newFile)

def console_output(access_key_id, secret_access_key, session_token, verbose):
    """ Outputs STS credentials to console """
    if verbose:
        print("Use these to set your environment variables:")
    exports = "\n".join([
        "export AWS_ACCESS_KEY_ID=%s" % access_key_id,
        "export AWS_SECRET_ACCESS_KEY=%s" % secret_access_key,
        "export AWS_SESSION_TOKEN=%s" % session_token
    ])
    print(exports)

    return exports


# pylint: disable=R0913
@click.command()
@click.option('-c', '--cache', is_flag=True, help='Cache the default profile credentials \
to ~/.okta-credentials.cache\n')
@click.option('-d', '--debug', is_flag=True, help='Enables debug mode')
@click.option('-f', '--force', is_flag=True, help='Forces new STS credentials. \
Skips STS credentials validation.')
@click.option('-t', '--token', help='TOTP token from your authenticator app')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-V', '--version', is_flag=True,
              help='Outputs version number and exits')
@click.option('-R', '--request', type=str, nargs=1, help="Pass a role to get access")
@click.option('-A', '--alias', type=str, nargs=1, help="Pass an alias to name it on ~/.aws/credentials")
@click.option('-r', '--roles', is_flag=True, help='Prints only Roles you have access to')
@click.option('--okta-profile', help="Name of the profile to use in .okta-aws. \
If none is provided, then the default profile will be used.\n")
@click.option('--profile', help="Name of the profile to store temporary \
credentials in ~/.aws/credentials. If profile doesn't exist, it will be \
created. If omitted, credentials will output to console.\n")
@click.argument('awscli_args', nargs=-1, type=click.UNPROCESSED)
def main(okta_profile, profile, verbose, version, request, alias, roles,
         debug, force, cache, awscli_args, token):
    """ Authenticate to awscli using Okta """
    if version:
        print(__version__)
        exit(0)
    # Set up logging
    logger = logging.getLogger('okta-awscli')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARN)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if verbose:
        handler.setLevel(logging.INFO)
    if debug:
        handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if not okta_profile:
        okta_profile = "default"
    aws_auth = AwsAuth(profile, okta_profile, verbose, logger)
    if roles:
        get_cred(
            aws_auth, okta_profile, verbose, logger, token, cache
        )
    elif request:
        if alias:
            if 1 ==1 :
                refresh_token(
                    aws_auth, okta_profile, profile, verbose, logger, token, cache, request, alias
                )
            else:
                pass
        else:
            if 1 ==1 :
                refresh_token(
                    aws_auth, okta_profile, profile, verbose, logger, token, cache, request
                )
            else:
                pass
    elif not aws_auth.check_sts_token(profile) or force:
        if force and profile:
            logger.info("Force option selected, \
                getting new credentials anyway.")
        elif force:
            logger.info("Force option selected, but no profile provided. \
                Option has no effect.")
        get_credentials(
            aws_auth, okta_profile, profile, verbose, logger, token, cache
        )

    if awscli_args:
        cmdline = ['aws', '--profile', profile] + list(awscli_args)
        logger.info('Invoking: %s', ' '.join(cmdline))
        call(cmdline)


if __name__ == "__main__":
    # pylint: disable=E1120
    main()
    # pylint: enable=E1120
