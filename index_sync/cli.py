import json
import random

import click
import requests
from faker import Faker
from flask.cli import with_appcontext
from invenio_pidstore.models import PersistentIdentifier, PIDStatus

CREATE_URL = 'https://127.0.0.1:5000/api/records/'
RECORD_URL = 'https://127.0.0.1:5000/api/records/{pid}'

fake = Faker()


def get_last_pid():
    """Get the last inserted PID."""
    try:
        pid = PersistentIdentifier.query.order_by(
            PersistentIdentifier.id.desc()
        ).first()
        return int(pid.id)
    except:
        return 1


def create_records(n_create):
    """Generate records."""
    start_pid = get_last_pid() + 1
    with click.progressbar(
        [i for i in range(start_pid, start_pid + n_create)],
        label='Creating {} record(s)...'.format(n_create)
    ) as record_pids:
        for pid in record_pids:
            n_keywords = random.randint(0, 5)
            n_contributors = random.randint(1, 6)

            keywords = []
            while len(keywords) < n_keywords:
                for keyword in fake.catch_phrase().split():
                    if len(keywords) >= n_keywords:
                        break
                    keywords.append(keyword)

            contributors = []
            for _ in range(n_contributors):
                n_ids = random.randint(1, 3)
                ids = [dict(source='', value=fake.uuid4()) for _ in range(n_ids)]
                affiliations = [fake.company() for _ in range(random.randint(0, 3))]
                contributors.append(dict(
                    ids=ids,
                    name=fake.name(),
                    affiliations=affiliations,
                    email=fake.ascii_email(),
                    role=random.choice(['ContactPerson', 'Researcher', 'Other'])
                ))

            record = dict(
                id=pid,
                title=fake.bs(),
                keywords=[keywords.pop() for _ in range(n_keywords)],
                publication_date=fake.date(pattern="%Y-%m-%d", end_datetime=None),
                contributors=contributors
            )
            requests.post(CREATE_URL, json=record, verify=False)


def delete_records(n_delete):
    """Delete records."""
    pids = random.sample([pid.id for pid in PersistentIdentifier.query.all()], n_delete)
    with click.progressbar(
        pids,
        label='Deleting {} record(s)...'.format(n_delete)
    ) as record_pids:
        for pid in record_pids:
            requests.delete(RECORD_URL.format(pid=pid), verify=False)


def update_records(n_update):
    """Update records."""
    pids = [
        pid.id
        for pid in PersistentIdentifier.query.filter(
            PersistentIdentifier.status != PIDStatus.DELETED
        ).all()
    ]
    with click.progressbar(
        random.sample(pids, n_update),
        label='Updating {} record(s)...'.format(n_update)
    ) as record_pids:
        for pid in record_pids:
            headers = {'content-type': 'application/json-patch+json'}
            ops = [
                dict(op='replace', path='/title', value=fake.bs())
            ]
            requests.patch(
                RECORD_URL.format(pid=pid),
                headers=headers,
                json=ops,
                verify=False
            )


@click.group()
def demo():
    """Demo data CLI."""


@demo.command()
@click.option("--create", "n_create", default=0)
@click.option("--delete", "n_delete", default=0)
@click.option("--update", "n_update", default=0)
@with_appcontext
def data(n_create, n_delete, n_update):
    """Insert demo data."""
    click.secho('Generating demo data', fg='yellow')

    if n_create > 0:
        create_records(n_create)

    if n_delete > 0:
        delete_records(n_delete)

    if n_update > 0:
        update_records(n_update)
