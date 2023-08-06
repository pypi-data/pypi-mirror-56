import os
from astropy import time
import astropy.units as u
from astropy.table import Table
from celery.task import PeriodicTask
from celery.utils.log import get_task_logger
from celery.local import PromiseProxy
import numpy as np
import pyvo.dal
import requests

client = pyvo.dal.TAPService('https://irsa.ipac.caltech.edu/TAP',)

def ztf_references():
    refstable = client.search("""
    SELECT field, fid, maglimit FROM ztf.ztf_current_meta_ref
    WHERE (nframes >= 15) AND (startobsdate >= '2018-02-05T00:00:00Z')
    AND (field < 2000)
    """).to_table()

    refs = refstable.group_by(['field', 'fid']).groups.aggregate(np.mean)
    refs = refs.filled()

    refs_grouped_by_field = refs.group_by('field').groups
    for field_id, rows in zip(refs_grouped_by_field.keys,
                              refs_grouped_by_field):
        print(field_id, rows)

ztf_references()
 
