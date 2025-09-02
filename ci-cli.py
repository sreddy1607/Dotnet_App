#!/usr/bin/env python3
import json
import argparse
import ast
import os
import sys
import urllib3

import requests

# Local modules (shipped with the CLI)
import login
import projects
import versioned_items
import labels
import label_versions
import deployment
import constants
import instances
import loginInput
import queries  # noqa: F401 (imported for other modules)
from typing import Optional

# ---- TLS / SSL ----
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Monkey patch requests to disable SSL verification globally
_original_post = requests.post
def _patched_post(*args, **kwargs):
    kwargs['verify'] = False
    return _original_post(*args, **kwargs)
requests.post = _patched_post


def mask_credentials_for_logging(credentials_string: str) -> str:
    """Safely mask credentials for logging (not used in CI token path)."""
    try:
        creds = json.loads(credentials_string)
        masked_creds = []
        for cred in creds:
            masked_cred = {}
            for key, value in cred.items():
                if key.lower() in ['apikey', 'password', 'token', 'secret']:
                    masked_cred[key] = '*' * 8
                else:
                    masked_cred[key] = value
            masked_creds.append(masked_cred)
        return json.dumps(masked_creds)
    except Exception:
        return "*** MASKED CREDENTIALS ***"


def load_credentials_from_json(file_path: str = "credentials.json") -> Optional[str]:
    """
    Load credentials from a JSON file and return as a JSON string.
    DO NOT print anything here to keep stdout clean for token capture.
    """
    try:
        if not os.path.exists(file_path):
            print(f"ERROR: Credentials file '{file_path}' not found!", file=sys.stderr)
            return None

        with open(file_path, 'r') as f:
            data = json.load(f)

        return json.dumps(data)

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in credentials file - {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to load credentials file - {e}", file=sys.stderr)
        return None


def parse_args():
    parent_parser = argparse.ArgumentParser(
        description="Sample Python CLI to perform MotioCI GraphQL API operations."
    )
    parent_parser.add_argument(
        '--server', type=str, required=True,
        help="Base URL for the MotioCI server (e.g. https://host)"
    )
    parent_parser.add_argument(
        '--non-interactive', action='store_true',
        help="CI-safe mode: disable interactive prompts and fail instead."
    )

    subject_parser = parent_parser.add_subparsers(dest="subject")

    # ---- login ----
    login_parser = subject_parser.add_parser(
        'login',
        help="Login to MotioCI and emit x-auth-token to stdout."
    )
    login_parser.add_argument(
        '--credentials', type=str, metavar='',
        help="Credentials JSON string (alternative to --credentialsFile)."
    )
    login_parser.add_argument(
        '--credentialsFile', type=str, default="credentials.json", metavar='',
        help="Path to JSON file containing credentials (default: credentials.json)."
    )

    # ---- instance ----
    instance_subparser = subject_parser.add_parser("instance", help="Queries on instances.")
    instance_verb_subparser = instance_subparser.add_subparsers(dest="verb")
    instance_ls_parser = instance_verb_subparser.add_parser("ls", help="List instances available to the user.")
    instance_ls_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")

    # ---- project ----
    project_subparser = subject_parser.add_parser("project", help="Queries on projects.")
    project_verb_subparser = project_subparser.add_subparsers(dest="verb")
    project_ls_parser = project_verb_subparser.add_parser("ls", help="List projects.")
    project_ls_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    project_ls_parser.add_argument('--instanceName', type=str, metavar='', help="Filter by instance name.")

    # ---- label ----
    label_subparser = subject_parser.add_parser("label", help="Queries/mutations on labels.")
    label_verb_subparser = label_subparser.add_subparsers(dest="verb")

    label_create_parser = label_verb_subparser.add_parser("create", help="Create a new label.")
    label_create_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    label_create_parser.add_argument('--instanceName', type=str, metavar='', help="Instance name.")
    label_create_parser.add_argument('--projectName', type=str, metavar='', help="Project name.")
    label_create_parser.add_argument('--name', type=str, metavar='', help="Label name to create.")
    label_create_parser.add_argument('--versionedItemIds', type=str, metavar='', help="List of item IDs.")

    label_ls_parser = label_verb_subparser.add_parser("ls", help="List labels.")
    label_ls_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    label_ls_parser.add_argument('--instanceName', type=str, metavar='', help="Instance name.")
    label_ls_parser.add_argument('--projectName', type=str, metavar='', help="Project name.")
    label_ls_parser.add_argument('--labelName', type=str, metavar='', help="Specific label name.")

    # ---- labelVersion ----
    label_version_subparser = subject_parser.add_parser("labelVersion", help="Queries on label versions.")
    label_version_verb_subparser = label_version_subparser.add_subparsers(dest="verb")
    label_version_ls_parser = label_version_verb_subparser.add_parser("ls", help="List label versions.")
    label_version_ls_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    label_version_ls_parser.add_argument('--instanceName', type=str, metavar='', help="Instance name.")
    label_version_ls_parser.add_argument('--projectName', type=str, metavar='', help="Project name.")
    label_version_ls_parser.add_argument('--labelName', type=str, metavar='', help="Label name.")

    # ---- deploy ----
    deployment_parser = subject_parser.add_parser("deploy", help="Execute a deployment.")
    deployment_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    deployment_parser.add_argument('--sourceInstanceId', type=int, metavar='', help="Source instance id.")
    deployment_parser.add_argument('--sourceInstanceName', type=str, metavar='', help="Source instance name.")

    label_source_group = deployment_parser.add_mutually_exclusive_group(required=True)
    label_source_group.add_argument('--labelId', type=int, metavar='', help="Source label id.")
    label_source_group.add_argument('--labelVersionId', type=int, metavar='', help="Source label version id.")
    label_source_group.add_argument('--versionedItemIds', type=str, metavar='', help="Create ad-hoc label with IDs.")
    label_source_group.add_argument('--searchPath', nargs='+', type=str, action='append', metavar='',
                                    help="Paths for ad-hoc label item discovery.")

    target_instance_group = deployment_parser.add_mutually_exclusive_group(required=True)
    target_instance_group.add_argument('--targetInstanceId', type=int, metavar='', help="Target instance id.")
    target_instance_group.add_argument('--targetInstanceName', type=str, metavar='', help="Target instance name.")
    target_instance_group.add_argument('--targetUnversionedInstanceId', type=int, metavar='', help="Unversioned id.")
    target_instance_group.add_argument('--targetUnversionedInstanceName', type=str, metavar='', help="Unversioned name.")

    deployment_parser.add_argument('--targetLabelName', type=str, metavar='', help="Target label name to create.")
    deployment_parser.add_argument('--projectName', type=str, metavar='', help="Target project name")
    deployment_parser.add_argument('--projectId', type=int, metavar='', help="Target project id")

    auth_group = deployment_parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('--camPassportId', type=str, metavar='', help="Portal authentication.")
    auth_group.add_argument('--username', type=str, metavar='', help="Standard authentication username.")
    deployment_parser.add_argument('--password', type=str, metavar='', help="Standard authentication password.")
    deployment_parser.add_argument('--namespaceId', type=str, metavar='', help="Namespace id (e.g., azure).")

    # ---- versionedItems ----
    vi_subparser = subject_parser.add_parser("versionedItems", help="Queries on versioned items.")
    vi_verb_subparser = vi_subparser.add_subparsers(dest="verb")
    vi_ls_parser = vi_verb_subparser.add_parser("ls", help="List versioned items.")
    vi_ls_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")
    vi_ls_parser.add_argument('--instanceName', type=str, metavar='', help="Instance name.")
    vi_ls_parser.add_argument('--projectName', type=str, metavar='', help="Project name.")
    vi_ls_parser.add_argument('--searchPath', type=str, metavar='', help="Search path string.")
    vi_ls_parser.add_argument('--currentOnly', type=bool, metavar='', help="True for current items only.")

    # ---- logout ----
    logout_parser = subject_parser.add_parser("logout", help="Logout of MotioCI.")
    logout_parser.add_argument('--xauthtoken', type=str, required=True, help="x-auth-token from login.")

    return parent_parser.parse_args()


def run_deployment(args):
    # Source instance
    if args.sourceInstanceId is None:
        source_instance_id = find_instance_id(args.sourceInstanceId, args.sourceInstanceName,
                                              "Enter Source Instance Name/Id: ")
    else:
        source_instance_id = args.sourceInstanceId

    # Source label input (mutually exclusive handled by argparse)
    if args.labelVersionId is not None:
        source_label_input = {'labelVersionId': args.labelVersionId}
    elif args.labelId is not None:
        source_label_input = {'labelId': args.labelId}
    elif args.versionedItemIds is not None:
        project_id = find_project_id(source_instance_id, args.projectId, args.projectName, "Enter Project Name/Id: ")
        ids_input_string = str(args.versionedItemIds)[1:-1]
        versionedItemIds = [int(v.strip()) for v in ids_input_string.split(",")]
        source_label_input = {'adHoc': {'versionedItemIds': versionedItemIds, 'projectId': project_id}}
    elif args.searchPath is not None:
        project_id = find_project_id(source_instance_id, args.projectId, args.projectName, "Enter Project Name/Id: ")
        source_label_input = {'adHoc': {'versionedItemIds': get_versioned_items_from_searchpaths(args, project_id),
                                        'projectId': project_id}}
    else:
        print("Error. Missing source input. Enter labelVersionId, labelId, versionedItemIds, or searchPath.")
        return

    # Target instance
    if args.targetInstanceId is not None or args.targetInstanceName is not None:
        if args.targetLabelName is not None:
            target_instance_id = find_instance_id(args.targetInstanceId, args.targetInstanceName,
                                                  "Enter Target Instance Name/Id:")
            deployment_target_input = {
                'instance': {
                    'id': target_instance_id,
                    'authentication': get_authentication(target_instance_id, True, args),
                    'labelName': args.targetLabelName
                }
            }
        else:
            print("Error. Missing target label name.")
            return
    elif args.targetUnversionedInstanceId is not None or args.targetUnversionedInstanceName is not None:
        target_instance_id = find_unversioned_instance_id(args.targetUnversionedInstanceId,
                                                          args.targetUnversionedInstanceName,
                                                          "Enter Target Unversioned Instance Name/Id:")
        deployment_target_input = {
            'unversionedInstance': {
                'id': target_instance_id,
                'authentication': get_authentication(target_instance_id, False, args)
            }
        }
    else:
        print("Error. Missing target input. Enter targetInstanceId/Name or targetUnversionedInstanceId/Name.")
        return

    deployment.deploy(source_label_input, source_instance_id, deployment_target_input)
    return


def get_available_namespaces(target_instance_id, is_versioned):
    variables = {'id': target_instance_id}
    if is_versioned:
        resp = requests.post(constants.GRAPH_URL, headers={'x-auth-token': constants.X_AUTH_TOKEN},
                             json={'query': queries.GET_VERSIONED_NAMESPACES, 'variables': variables})
        return resp.json()["data"]["instance"]["namespaces"]
    else:
        resp = requests.post(constants.GRAPH_URL, headers={'x-auth-token': constants.X_AUTH_TOKEN},
                             json={'query': queries.GET_UNVERSIONED_NAMESPACES, 'variables': variables})
        return resp.json()["data"]["unversionedInstance"]["namespaces"]


def complete_standard_auth(namespaces, args):
    """Build password auth block. Honors --non-interactive (no prompts)."""
    valid_namespaces = [ns['id'] for ns in namespaces]

    # Password
    if args.password is None:
        if getattr(args, "non_interactive", False):
            print("ERROR: --password is required in --non-interactive mode.", file=sys.stderr)
            sys.exit(2)
        print("Username Entered: ", args.username)
        password = input("Enter Password: ")
    else:
        password = args.password

    # Namespace (CLI -> env -> default 'azure' if present -> prompt)
    namespace_id_input = args.namespaceId or os.environ.get("NAMESPACE_ID")
    if not namespace_id_input and "azure" in valid_namespaces:
        namespace_id_input = "azure"

    # Validate or prompt
    if not namespace_id_input or namespace_id_input not in valid_namespaces:
        if getattr(args, "non_interactive", False):
            print(f"ERROR: Invalid or missing namespaceId. Valid options: {valid_namespaces}", file=sys.stderr)
            sys.exit(2)
        while not namespace_id_input or namespace_id_input not in valid_namespaces:
            print("Invalid or missing namespaceId. Available namespaces:", valid_namespaces)
            namespace_id_input = input("Enter namespaceId (or 'q' to quit): ")
            if namespace_id_input == "q":
                print("Aborted by user.", file=sys.stderr)
                sys.exit(1)

    return {
        'password': {
            'namespaceId': namespace_id_input,
            'username': args.username,
            'password': password
        }
    }


def get_authentication(target_instance_id, is_versioned, args):
    if args.camPassportId is not None:
        return {'camPassportId': args.camPassportId}
    elif args.username is not None:
        namespaces = get_available_namespaces(target_instance_id, is_versioned)
        return complete_standard_auth(namespaces, args)
    else:
        print("Error. Missing deployment credentials. Enter camPassportId or username/password.", file=sys.stderr)
        sys.exit(2)


def find_instance_id(instance_id, instance_name, input_string):
    outputOptionsAvailable = False
    instance_array = instances.get_instances_default()
    while True:
        if instance_id is None:
            if instance_name is None:
                if outputOptionsAvailable:
                    instance_array = instances.get_instances_default()
                    print("Error! Incorrect Input!")
                    print("Available entries: ", end="")
                    instances.print_instances(instance_array)
                    print("")
                user_input = input(input_string)
                outputOptionsAvailable = True
                instance_id, instance_name = assign_input(user_input)

        if instance_id is not None:
            if instances.check_if_valid_instance_id(instance_array, instance_id):
                break

        elif instance_name is not None:
            if instances.check_if_valid_instance_name(instance_array, instance_name):
                instance_id = instances.get_instance_id(instance_name)
                break

        instance_id = None
        instance_name = None
    return instance_id


def find_unversioned_instance_id(instance_id, instance_name, input_string):
    outputOptionsAvailable = False
    instance_array = instances.get_unversioned_instances_default()
    while True:
        if instance_id is None:
            if instance_name is None:
                if outputOptionsAvailable:
                    instance_array = instances.get_unversioned_instances_default()
                    print("Error! Incorrect Input!")
                    print("Available entries: ", end="")
                    instances.print_instances(instance_array)
                    print("")
                user_input = input(input_string)
                outputOptionsAvailable = True
                instance_id, instance_name = assign_input(user_input)

        if instance_id is not None:
            if instances.check_if_valid_instance_id(instance_array, instance_id):
                break

        elif instance_name is not None:
            if instances.check_if_valid_instance_name(instance_array, instance_name):
                instance_id = instances.get_unversioned_instance_id(instance_name)
                break

        instance_id = None
        instance_name = None
    return instance_id


def find_project_id(source_instance_id, project_id, project_name, input_string):
    outputOptionsAvailable = False
    project_list = projects.get_valid_projects(source_instance_id)
    while True:
        if project_id is None:
            if project_name is None:
                if outputOptionsAvailable:
                    print("Error! Incorrect Input!")
                    print("Available entries: ", end="")
                    project_list = projects.get_valid_projects(source_instance_id)
                    projects.print_projects(project_list)
                    print("")
                user_input = input(input_string)
                outputOptionsAvailable = True
                project_id, project_name = assign_input(user_input)

        if project_id is not None:
            if projects.check_if_valid_project_id(project_list, project_id):
                break

        elif project_name is not None:
            if projects.check_if_valid_project_name(project_list, project_name):
                project_id = projects.get_project_id(source_instance_id, project_name)
                break

        project_id = None
        project_name = None
    return project_id


def assign_input(user_input):
    try:
        int_input = int(user_input)
        return int_input, None
    except ValueError:
        return None, user_input


def get_user_input_versioned_item_ids():
    versioned_item_ids = []
    print("Enter versionedItemIds. Press q to stop:")
    while True:
        curId = input("Enter id:")
        if curId == "q":
            break
        response = versioned_items.get_versioned_item_by_id(int(curId))
        if response["data"]["versionedItem"] is None:
            print("Bad versionedItemId, enter another one")
            continue
        versioned_item_ids.append(int(curId))
    return versioned_item_ids


def get_versioned_items_from_searchpaths(args, project_id):
    versioned_item_ids = []
    versioned_item_ids.extend(ast.literal_eval(label_versions.get_version_ids(project_id, args.searchPath)))
    return versioned_item_ids


# ---------------- MAIN ----------------
args = parse_args()
constants.CI_URL = args.server
constants.LOGIN_URL = constants.CI_URL + constants.LOGIN_URL
constants.LOGOUT_URL = constants.CI_URL + constants.LOGOUT_URL
constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL

if args.subject == "login":
    # Priority: --credentials -> --credentialsFile
    if args.credentials is not None:
        credentials_to_use = args.credentials
    else:
        credentials_to_use = load_credentials_from_json(args.credentialsFile)
        if credentials_to_use is None:
            print("ERROR: No credentials provided and credentialsFile not found/invalid.", file=sys.stderr)
            sys.exit(1)

    token = login.login_init(credentials_to_use)
    if not token:
        print("ERROR: Login failed (no token returned).", file=sys.stderr)
        sys.exit(1)

    # IMPORTANT: print ONLY the token. No extra text.
    print(token)
    sys.exit(0)
else:
    # Sanitize token in case caller passed with newline/spaces
    constants.X_AUTH_TOKEN = (args.xauthtoken or "").strip()

# Dispatch
if args.subject == "instance":
    if args.verb == "ls":
        print(instances.get_instances_default())

elif args.subject == "project":
    if args.verb == "ls":
        if args.instanceName is not None:
            projects.get_projects_specific(args.instanceName)
        else:
            projects.get_projects_default()

elif args.subject == "label":
    if args.verb == "create":
        labels.create_label_init(args.instanceName, args.projectName, args.name, args.versionedItemIds)
        print("Label Created!")
    elif args.verb == "ls":
        if args.labelName is not None:
            labels.get_label_specific(args.instanceName, args.projectName, args.labelName)
        elif args.instanceName is not None and args.projectName is not None:
            labels.get_labels_specific(args.instanceName, args.projectName)
        else:
            labels.get_labels_default()

elif args.subject == "deploy":
    run_deployment(args)

elif args.subject == "labelVersion":
    if args.verb == "ls":
        if args.instanceName is not None and args.projectName is not None and args.labelName is not None:
            label_versions.get_label_version_specific(args.instanceName, args.projectName, args.labelName)
        else:
            label_versions.get_label_version_default()

elif args.subject == "versionedItems":
    if args.verb == "ls":
        if (args.instanceName is not None and args.projectName is not None and
                args.searchPath is not None and args.currentOnly is not None):
            versioned_items.get_versioned_items_specific(
                args.instanceName, args.projectName, args.searchPath, args.currentOnly
            )
        else:
            versioned_items.get_versioned_items_default()

elif args.subject == "logout":
    requests.post(constants.LOGOUT_URL, headers={'x-auth-token': constants.X_AUTH_TOKEN})
    print("Logged out!")
