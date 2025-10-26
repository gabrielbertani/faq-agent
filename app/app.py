import streamlit as st
import asyncio, threading, queue

import ingest
import search_agent
import logs


# --- Initialization ---
@st.cache_resource
def init_agent():
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    def filter(doc):
        return "data-engineering" in doc["filename"]

    st.write("🔄 Indexing repo...")
    index = ingest.index_data(repo_owner, repo_name, filter=filter)
    agent = search_agent.init_agent(index, repo_owner, repo_name)
    return agent


agent = init_agent()

# --- Streamlit UI ---
st.set_page_config(page_title="AI FAQ Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI FAQ Assistant")
st.caption("Ask me anything about the DataTalksClub/faq repository")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Streaming helper ---
def stream_response(prompt: str):
    import asyncio, threading, queue
    q = queue.Queue()
    DONE = object()

    def runner():
        async def task():
            async with agent.run_stream(user_prompt=prompt) as result:
                async for chunk in result.stream_output(debounce_by=0.01):
                    # pydantic-ai pode entregar objeto; pegue o texto
                    text = getattr(chunk, "text", chunk)
                    if not isinstance(text, str):
                        text = str(text)
                    q.put(text)
                # guarda resposta completa e logs
                full = await result.get_output_str()
                st.session_state._last_response = full
                logs.log_interaction_to_file(agent, result.new_messages())
            q.put(DONE)

        asyncio.run(task())

    threading.Thread(target=runner, daemon=True).start()

    while True:
        item = q.get()
        if item is DONE:
            return
        yield item


# --- Chat input ---
if prompt := st.chat_input("Ask your question..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message (streamed)
    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_response(prompt))

    # Save full response to history
    final_text = getattr(st.session_state, "_last_response", response_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})

