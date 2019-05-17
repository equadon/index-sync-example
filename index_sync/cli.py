import json
import random

import click
from faker import Faker
from flask.cli import with_appcontext
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records.api import Record

fake = Faker()


def minter(pid_type, pid_field, record):
    """Mint the given PID for the given record."""
    PersistentIdentifier.create(
        pid_type=pid_type,
        pid_value=record[pid_field],
        object_type="rec",
        object_uuid=record.id,
        status=PIDStatus.REGISTERED,
    )


def create_records(start_pid, n_records):
    """Generate records."""
    record_ids = [i for i in range(start_pid, start_pid + n_records)]
    records = []
    with click.progressbar(
        record_ids,
        label='Creating {} record(s)...'.format(n_records)
    ) as bar:
        for i in bar:
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
                id=i,
                title=fake.bs(),
                keywords=[keywords.pop() for _ in range(n_keywords)],
                publication_date=fake.date(pattern="%Y-%m-%d", end_datetime=None),
                contributors=contributors
            )
            record = Record.create(record)
            minter('recid', 'id', record)
            record.commit()
            records.append(record)
    return records


@click.group()
def demo():
    """Demo data CLI."""


@demo.command()
@click.option("--records", "n_records", default=100)
@click.option("--start-pid", "start_pid", default=1)
@with_appcontext
def data(n_records, start_pid):
    """Insert demo data."""
    click.secho('Generating demo data', fg='yellow')

    indexer = RecordIndexer()

    records = create_records(start_pid, n_records)
    db.session.commit()

    click.secho('Indexing {} record(s)...'.format(len(records)), fg='green')
    indexer.bulk_index([str(r.id) for r in records])
    indexer.process_bulk_queue()
