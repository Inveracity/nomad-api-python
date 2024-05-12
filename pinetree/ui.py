import time

import pandas as pd
import streamlit as st

from pinetree import nomad
from pinetree.models import JobVars

STATUS = {"running": "✅"}


def frontend():
    with st.spinner("Getting apps"):
        allocs = nomad.get_all()
        data = []
        column_names = ["apps", "Status"]
        for alloc in allocs:
            data.append(
                (
                    f"http://localhost/{alloc.Name}",
                    STATUS.get(alloc.Status, alloc.Status),
                )
            )

        df = pd.DataFrame(data, columns=column_names)
        st.dataframe(df, column_config={"apps": st.column_config.LinkColumn()}, hide_index=True)

    # Inputs
    st.text_input(label="image", value="traefik/whoami:v1.10", key="image")
    st.text_input(label="name", value="my app", key="name")
    st.text_input(label="datacenter", value="dc1", key="datacenter")
    st.number_input(label="port", min_value=80, max_value=66535, key="port")
    st.button(label="deploy", on_click=deploy_container)


def deploy_container():
    st.toast("App deployment request received", icon="👍")
    with st.spinner("Deploying"):
        job_vars = JobVars(
            name="-".join(st.session_state["name"].split()),
            image=st.session_state["image"],
            port=st.session_state["port"],
            datacenter=st.session_state["datacenter"],
        )
        job_payload = nomad.job_create(job_vars=job_vars)
        nomad.deploy(job_payload)
        time.sleep(5)
    st.toast("App deployed, it can take a minute to go live", icon="🎉")
