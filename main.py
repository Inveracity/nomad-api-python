import asyncio
import os
from pathlib import Path

import jinja2
from httpx import AsyncClient


RenderedTemplate = str
JobJson = dict

NOMAD_TOKEN = os.environ.get("NOMAD_TOKEN")
NOMAD_ADDR = os.environ.get("NOMAD_ADDR")


async def main():
    client = AsyncClient(headers={"X-Nomad-Token": NOMAD_TOKEN})

    job = await parse(client, render_template())
    await deploy(client, job)
    await get(client, "test")
    await client.aclose()


async def parse(client: AsyncClient, job: RenderedTemplate) -> JobJson:
    """Convert job HCL string to JSON"""
    resp = await client.post(
        f"{NOMAD_ADDR}/v1/jobs/parse",
        json={
            "JobHCL": job,
            "Canonicalize": True,
        },
    )
    return resp.json()


async def get(client: AsyncClient, _id: str):
    """Get job details"""
    response = await client.get(
        f"{NOMAD_ADDR}/v1/job/{_id}",
    )

    print(response.json())


async def deploy(client: AsyncClient, job: JobJson):

    register_job_as_dict = {
        "EnforceIndex": False,
        "PreserveCounts": True,
        "PolicyOverride": False,
        "JobModifyIndex": 0,
        "Job": job,
    }

    response = await client.post(f"{NOMAD_ADDR}/v1/jobs", json=register_job_as_dict)

    print(response.json())


def render_template() -> RenderedTemplate:
    job_template = Path("./job.hcl.j2").read_text()
    t = jinja2.Template(job_template)
    job_vars = {
        "job": {
            "name": "test",
            "image": "traefik/whoami:latest",
            "port": "80",
        },
    }

    return t.render(job_vars)


if __name__ == "__main__":
    asyncio.run(main())
