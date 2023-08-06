import sys
import csv
import collections

import gitlab

from gitlabevents.log import Logger
from gitlabevents.args import get_args

log    = Logger()
arg    = get_args()
server = arg.server
token  = arg.token
gl     = None

path   = arg.output
if not path:
    path   = sys.stdout.fileno()

def gl_auth(server, token):
    global gl
    log.info("Connecting to %s..." % (server))
    gl = gitlab.Gitlab(server, private_token=token)
    try:
        gl.auth()
    except:
        log.failur("Connection refused")
        exit(-1)
    log.success("Auth complete")

def get_user(user_id):
    """
    Caching users in dictionary to reduce actual number of requests to api
    """
    global gl
    if not get_user.users[user_id]:
        get_user.users[user_id] = gl.users.get(user_id)
    return get_user.users[user_id]
get_user.users = collections.defaultdict(lambda: None)

def prepare_event(event, project):
    """
    Removing needless elements from attriubtes and adding some new
    """
    trash_list = [
        'author',
        'push_data',
        'target_title',
        'target_type',
        'target_id',
        'target_iid',
        'note',
    ]
    event['author_name'] = event['author']['name']
    event['project_name'] = project.attributes['name']
    event['project_name_with_namespace'] = project.attributes['name_with_namespace']

    user = get_user(event['author_id']).attributes
    if not 'created_at' in user:
        log.warn('Failed to get creation date of user %s' % (user['name']))
        event['user_created'] = 'unknown'
    else:
        event['user_created'] = user['created_at']

    for trash in trash_list:
        if trash in event.keys():
            del event[trash]

def push_values(table, projects):
    """
    Adds the list of values of each event for every project in projects
    """
    for project in projects:
        events = project.events.list()
        for event in events:
            event = event.attributes
            prepare_event(event, project)
            table.append([v for (k, v) in event.items()])

def main():
    global gl
    gl_auth(server, token)

    log.info("Fetching projects list")
    projects = gl.projects.list(all=True)

    log.info("Generating csv header")
    events = projects[0].events.list()
    event = events[0].attributes

    prepare_event(event, projects[0])

    table = []
    table.append([k for k in event]) #adding header for result table

    log.info("Pushing values to csv table")
    push_values(table, projects)

    log.info("Wrinting result to file")
    try:
        with open(path, "w", newline="") as output:
            writer = csv.writer(output, delimiter=",")
            for line in table:
                writer.writerow(line)
    except:
        log.failure("Failed to open file")
        exit(-1)
    log.success("Done!")

