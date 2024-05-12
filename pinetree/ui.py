import time

import streamlit as st

from pinetree import nomad
from pinetree.models import JobVars


def frontend():
    st.write(nomad.get_all())
    st.text_input(label="image", value="traefik/whoami:latest", key="image")
    st.text_input(label="name", value="my app", key="name")
    st.text_input(label="datacenter", value="dc1", key="datacenter")
    st.number_input(label="port", min_value=80, max_value=66535, key="port")
    st.button(label="deploy", on_click=deploy_container)


def deploy_container():
    with st.spinner("Deploying"):
        job_vars = JobVars(
            name="-".join(st.session_state["name"].split()),
            image=st.session_state["image"],
            port=st.session_state["port"],
            datacenter=st.session_state["datacenter"],
        )
        print(job_vars)
        job_payload = nomad.job_create(job_vars=job_vars)
        # print(job_payload)
        resp = nomad.deploy(job_payload)
        print(resp)

    # st.write(resp)
    name = "-".join(st.session_state["name"].split())
    st.success(f"Deployed {st.session_state['image']} to https://{name}.christopherbaklid.com")
