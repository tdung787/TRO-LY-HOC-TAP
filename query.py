from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from src.global_settings import INDEX_STORAGE
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import Settings
import streamlit as st

openai.api_key = st.secrets.openai.OPENAI_API_KEY
Settings.llm = OpenAI(model="gpt-4o", temperature=0.2)

storage_context = StorageContext.from_defaults(
    persist_dir=INDEX_STORAGE
)
index = load_index_from_storage(
    storage_context, index_id="vector"
)
query_engine = index.as_query_engine(
    similarity_top_k=1,
    streaming=True
)

response = query_engine.query("Sự không phân li của một cặp NST ở một số tế bào trong giảm phân hình thành giao tử ở một bên bố hoặc mẹ, qua thụ tinh có thể hình thành các hợp tử mang bộ NST là?"
"Hãy giải thích?")

print(response)

