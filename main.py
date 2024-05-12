import asyncio
import os
from pathlib import Path

import jinja2
from httpx import Client

RenderedTemplate = str
JobJson = dict

NOMAD_TOKEN = os.environ.get("NOMAD_TOKEN")
NOMAD_ADDR = os.environ.get("NOMAD_ADDR")


def main():
    client = Client(headers={"X-Nomad-Token": NOMAD_TOKEN})

    job = parse(client, render_template())
    deploy(client, job)
    get(client, "test")
    client.close()


def parse(client: Client, job: RenderedTemplate) -> JobJson:
    """Convert job HCL string to JSON"""
    resp = client.post(
        f"{NOMAD_ADDR}/v1/jobs/parse",
        json={
            "JobHCL": job,
            "Canonicalize": True,
        },
    )
    return resp.json()


def get(client: Client, _id: str):
    """Get job details"""
    response = client.get(
        f"{NOMAD_ADDR}/v1/job/{_id}",
    )

    print(response.json())


def deploy(client: Client, job: JobJson):

    register_job_as_dict = {
        "EnforceIndex": False,
        "PreserveCounts": True,
        "PolicyOverride": False,
        "JobModifyIndex": 0,
        "Job": job,
    }

    response = client.post(f"{NOMAD_ADDR}/v1/jobs", json=register_job_as_dict)

    print(response.json())


def render_template() -> RenderedTemplate:
    job_template = Path("./job.hcl.j2").read_text()
    t = jinja2.Template(job_template)
    job_vars = {
        "job": {
            "name": "test",
            "datacenter": "dc1",
            "image": "traefik/whoami:latest",
            "port": "80",
        },
    }

    return t.render(job_vars)


if __name__ == "__main__":
    main()
