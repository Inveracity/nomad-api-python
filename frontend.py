import time

import streamlit as st


def frontend():
    st.text_input(label="image", value="traefik/whoami:latest", key="image")
    st.text_input(label="name", value="my app", key="name")
    st.number_input(label="port", min_value=80, max_value=66535, key="port")

    def mycallback():
        with st.spinner("Deploying"):
            time.sleep(5)
        name = "-".join(st.session_state["name"].split())
        st.success(f"Deployed {st.session_state['image']} to https://{name}.christopherbaklid.com")

    st.button(label="deploy", on_click=mycallback)


frontend()
