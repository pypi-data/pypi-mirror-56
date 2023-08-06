import os
import random
import StringIO
import time

from pvHelpers.utils import CaseInsensitiveDict, randUnicode
from werkzeug.datastructures import FileStorage


def get_members(org_id, crypto_client):
    existing_users = CaseInsensitiveDict(
        {u['user_id']: u for u in crypto_client.list_local_users()['users']})
    return CaseInsensitiveDict({
        uid: u for uid, u in existing_users.iteritems() if
             u['org_info'] and u['org_info']['org_id'] == org_id
    })


def send_email(sender, recipients, crypto_client):
    subject = randUnicode()
    text = randUnicode()
    tos = recipients
    ccs = []
    bccs = []
    html = u'<div>{}</div>'.format(randUnicode())
    atts = [{
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'image/jpeg'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'application/zip'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'audio/jpeg'
    }, {
        'content': os.urandom(1024),
        'name': randUnicode(),
        'type': 'application/pdf'
    }]

    attachments = [
        FileStorage(
            stream=StringIO.StringIO(a['content']),
            filename=a['name'], content_type=a['type']) for a in atts]

    crypto_client.send_email(
        4, {'user_id': sender['user_id'], 'display_name': sender['display_name']},
        [{'user_id': t['user_id'], 'display_name': t['display_name']} for t in tos],
        [{'user_id': c['user_id'], 'display_name': c['display_name']} for c in ccs],
        [{'user_id': b['user_id'], 'display_name': b['display_name']} for b in bccs],
        subject, text, html, attachments, None, [], [], [])


def create_export_group(admin, members, optionals_required, crypto_client):
    group = crypto_client.create_org_approval_group(
        admin['user_id'], admin['org_info']['org_id'], 'export_group', members, optionals_required)

    crypto_client.set_roled_approval_group(
        admin['user_id'], admin['org_info']['org_id'], group['id'], group['version'], 'export_approval_group')

    return group


def add_member(admin, crypto_client, cs_client, member_id=None, department=None, role='standard'):
    member_id = member_id or u'{}@preveil.test'.format(randUnicode())
    department = department or randUnicode()

    crypto_client.invite_org_member(
        admin['user_id'], admin['org_info']['org_id'], member_id, randUnicode(), department, role)
    d = cs_client.get_user_secret(member_id, u'account_setup')
    member = crypto_client.claim_account(member_id, d['secret'], d['metadata']['key_version'])
    if role == 'admin':
        crypto_client.change_member_role(admin['user_id'], admin['org_info']['org_id'], member_id, role)
        member['org_info']['role'] = u'admin'

    return member


def create_new_org(admin_id, crypto_client):
    admin = crypto_client.create_test_account(admin_id, u'journal')
    crypto_client.create_organization(admin_id)['org_id']
    existing_users = CaseInsensitiveDict(
        {u['user_id']: u for u in crypto_client.update_and_list_local_users(admin_id)['users']})
    admin = existing_users[admin_id]
    return admin


class Timings:
    NEW_EMAIL = (int(os.environ.get('NEW_EMAIL', 10)), 0)
    NEW_MEMBER = (int(os.environ.get('NEW_MEMBER', 100)), 0)

    # EXPORT_GROUP_CHANGE
    # MEMBER_REKEY


def generate_load(admin_id, backend_client, crypto_client):
    existing_users = CaseInsensitiveDict(
        {u['user_id']: u for u in crypto_client.update_and_list_local_users(admin_id)['users']})
    admin = existing_users[admin_id]
    org_id = admin['org_info']['org_id']
    while True:
        current_time = time.time()

        # take a random member
        if current_time - Timings.NEW_MEMBER[1] > Timings.NEW_MEMBER[0]:
            add_member(admin, crypto_client, backend_client)

            Timings.NEW_MEMBER = (Timings.NEW_MEMBER[0], time.time())

        if current_time - Timings.NEW_EMAIL[1] > Timings.NEW_EMAIL[0]:
            members = get_members(org_id, crypto_client).values()
            sender = random.choice(members)
            recipients = random.sample(members, random.randint(1, len(members)))

            send_email(sender, recipients, crypto_client)

            Timings.NEW_EMAIL = (Timings.NEW_EMAIL[0], time.time())

        time.sleep(0.01)
