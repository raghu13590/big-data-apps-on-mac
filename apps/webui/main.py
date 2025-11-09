import streamlit as st
import docker
import os
import subprocess
from pathlib import Path

st.set_page_config(page_title="Docker Service Manager", layout="wide")

client = docker.from_env()

def get_containers():
    containers = []
    for c in client.containers.list(all=True):
        containers.append({
            'id': c.id,
            'name': c.name,
            'image': c.image.tags[0] if c.image.tags else str(c.image),
            'status': c.status
        })
    return containers

def get_container_logs(cid, tail=100):
    container = client.containers.get(cid)
    try:
        logs = container.logs(tail=tail).decode('utf-8')
    except Exception as e:
        logs = f"Error fetching logs: {e}"
    return logs

def start_container(cid):
    container = client.containers.get(cid)
    container.start()

def stop_container(cid):
    container = client.containers.get(cid)
    container.stop()

def restart_container(cid):
    container = client.containers.get(cid)
    container.restart()


def main():
    st.title('Docker Service Manager')
    st.markdown('Manage your Docker containers visually')

    st.header('Docker Containers')
    containers = get_containers()

    if not containers:
        st.info('No containers found.')
    else:
        # Group containers by the first part of their image (before colon or dash)
        from collections import defaultdict
        import re
        groups = defaultdict(list)
        for c in containers:
            # Extract group from image: before first colon or dash
            image = c['image']
            m = re.match(r"([\w\-/]+?)[-:].*", image)
            group = m.group(1) if m else image
            groups[group].append(c)

        for group_name in sorted(groups.keys()):
            with st.expander(f"{group_name} ({len(groups[group_name])})", expanded=True):
                for c in groups[group_name]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(f"{c['name']}")
                        st.write(f"Image: {c['image']}")
                        status_color = {'running': 'green', 'exited': 'red', 'paused': 'orange'}.get(c['status'], 'grey')
                        st.markdown(f"<span style='color:{status_color};font-weight:bold;'>Status: {c['status'].capitalize()}</span>", unsafe_allow_html=True)
                    with col2:
                        if c['status'] == 'running':
                            if st.button(f"Stop {c['name']}"):
                                stop_container(c['id'])
                                st.experimental_rerun()
                            if st.button(f"Restart {c['name']}"):
                                restart_container(c['id'])
                                st.experimental_rerun()
                        else:
                            if st.button(f"Start {c['name']}"):
                                start_container(c['id'])
                                st.experimental_rerun()

                    # Show logs button and display
                    log_state_key = f"show_logs_{c['id']}"
                    log_btn_key = f"btn_show_logs_{c['id']}"
                    if log_state_key not in st.session_state:
                        st.session_state[log_state_key] = False

                    if st.button(
                        f"{'Hide' if st.session_state[log_state_key] else 'Show'} Logs for {c['name']}", key=log_btn_key
                    ):
                        st.session_state[log_state_key] = not st.session_state[log_state_key]

                    if st.session_state[log_state_key]:
                        logs = get_container_logs(c['id'], tail=200)
                        st.text_area(
                            f"Logs: {c['name']}",
                            logs,
                            height=400,
                            key=f"logs_area_{c['id']}",
                            args=None,
                            disabled=True
                        )
                        st.markdown("<style>textarea { resize: vertical; width: 100% !important; }</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()