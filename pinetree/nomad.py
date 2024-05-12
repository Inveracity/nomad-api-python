import os
from pathlib import Path
from typing import List

import jinja2
from httpx import Client

from pinetree.models import Alloc, JobJson, JobVars, RenderedTemplate

NOMAD_TOKEN = os.environ.get("NOMAD_TOKEN")
NOMAD_ADDR = os.environ.get("NOMAD_ADDR")

client = Client(headers={"X-Nomad-Token": NOMAD_TOKEN})


def _parse(job: RenderedTemplate) -> JobJson:
    """Convert job HCL string to JSON"""
    resp = client.post(
        f"{NOMAD_ADDR}/v1/jobs/parse",
        json={
            "JobHCL": job,
            "Canonicalize": True,
        },
    )
    return resp.json()


def get_all() -> List[Alloc]:
    """Get job details"""
    response = client.get(
        f"{NOMAD_ADDR}/v1/jobs",
    )
    return [Alloc(**x) for x in response.json()]


def deploy(job: JobJson) -> dict:

    register_job_as_dict = {
        "EnforceIndex": False,
        "PreserveCounts": True,
        "PolicyOverride": False,
        "JobModifyIndex": 0,
        "Job": job,
    }

    response = client.post(f"{NOMAD_ADDR}/v1/jobs", json=register_job_as_dict)
    return response.json()


def job_create(job_vars: JobVars) -> JobJson:
    job_template = Path("./nomad/job.hcl.j2").read_text()
    t = jinja2.Template(job_template)
    return _parse(t.render(job_vars.model_dump()))
