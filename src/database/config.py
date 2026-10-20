import httpx
import streamlit as st
from supabase import create_client, ClientOptions

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
    options=ClientOptions(
        httpx_client=httpx.Client(http2=False, timeout=15),
    ),
)