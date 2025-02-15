import streamlit as st
import streamlit_shadcn_ui as ui
import time
import main

def notification(value: str):
    values = ('already_exists', 'blocked', 'unblocked')
    if value == values[0]:
        st.toast(f'Already Exists: {input_value}',icon='🚫')
    if value == values[1]:
        st.toast(f'Blocked: {input_value}',icon='✋')
    if value == values[2]:
        st.toast(f'UnBlocked: {input_value}',icon='🔓')

st.header("Web Blocker")

st.logo(
    image="icons/app_blocking.png", size="large", link=None, icon_image=None
)
st.sidebar.write("hallo semua")

value = ui.tabs(options=['All', 'Block', 'UnBlock'], default_value='All', key="tabs")

if value == "All":
    st.subheader("All Blocked")
    text = ""
    at = main.show_blocked()
    for line in at:
        text += line.split(" ")[-1]
    st.text(text)

elif value == "Block":
    st.subheader("Block Websites")
    input_value = ui.input(default_value="", type='text', placeholder="Enter text here", key="input1")
    blocked = ui.button("Click", key="clk_btn")
    if blocked and input_value:
        if main.is_website_blocked(input_value):
            notification('already_exists')
        else:
            main.block_website(input_value)
            notification('blocked')

elif value == "UnBlock":
    st.subheader("UnBlock Websites")
    input_value = ui.input(default_value="", type='text', placeholder="Enter text here", key="input1")
    blocked = ui.button("Click", key="clk_btn")
    if blocked and input_value != "":
        main.unblock_website(input_value)
        notification('unblocked')

