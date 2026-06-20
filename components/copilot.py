# GreenMind AI - AI Sustainability Copilot (RAG Chat)

import streamlit as st
from utils.rag_store import RAGStore
from utils.ai_helper import generate_rag_answer

@st.cache_resource
def get_rag_store():
    """Caches the RAG store indexing so it only loads once."""
    return RAGStore(kb_dir="knowledge_base")

def render_copilot():
    # Page Header
    st.markdown("<h1 class='gradient-text' style='margin-bottom:5px;'>AI Sustainability Copilot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem;'>Ask anything about campus energy, water, waste, or SDG targets. Answers are grounded in verified policy documents.</p>", unsafe_allow_html=True)
    
    # Load RAG store
    store = get_rag_store()
    
    # ------------------ EXAMPLE QUESTIONS ------------------
    with st.container(border=True):
        st.markdown("<h5 style='margin:0 0 10px 0; color:#3b82f6;'>Suggested Queries (Click to paste):</h5>", unsafe_allow_html=True)
        
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("How can our campus reduce electricity consumption?"):
                st.session_state.suggested_query = "How can our campus reduce electricity consumption?"
            if st.button("What actions can reduce our carbon footprint?"):
                st.session_state.suggested_query = "What actions can reduce our carbon footprint?"
                
        with col_q2:
            if st.button("How can we improve SDG alignment on campus?"):
                st.session_state.suggested_query = "How can we improve SDG alignment on campus?"
            if st.button("What are the rainwater harvesting potential rules?"):
                st.session_state.suggested_query = "What are the rainwater harvesting potential rules?"
    
    # ------------------ CHAT CONVERSATION WINDOW ------------------
    # Retrieve active query from click or input
    user_query = st.chat_input("Enter your sustainability question here...")
    
    # Check if a suggested query was clicked
    if "suggested_query" in st.session_state and st.session_state.suggested_query:
        user_query = st.session_state.suggested_query
        # Clear it immediately so it doesn't loop
        st.session_state.suggested_query = None
        
    # Render historical chat log
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("Grounded RAG References"):
                    for idx, src in enumerate(message["sources"]):
                        st.markdown(f"**Source {idx+1}: {src['source']}** (Match Strength: {src['score']:.2f})")
                        st.markdown(f"*{src['text']}*")
                        st.markdown("---")

    # Handle new query submission
    if user_query:
        # Rate Limiting Logic (Max 15 queries per session)
        if "query_count" not in st.session_state:
            st.session_state.query_count = 0
            
        if st.session_state.query_count >= 15:
            st.error("⚠️ Session limit reached (15 queries) to prevent API abuse. Please refresh the page or clear chat to start a new session.")
            st.stop()
            
        st.session_state.query_count += 1

        # Display user question
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # Append to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Retrieve context from RAG store
        with st.spinner("Searching sustainability knowledge base..."):
            retrieved_chunks = store.retrieve(user_query, top_k=3)
            
        # Call Gemini model
        with st.spinner("Synthesizing response..."):
            answer = generate_rag_answer(user_query, retrieved_chunks, chat_history=st.session_state.chat_history)
            
        # Display AI answer
        with st.chat_message("assistant"):
            st.markdown(answer)
            # Display source accordion
            with st.expander("Grounded RAG References"):
                for idx, src in enumerate(retrieved_chunks):
                    st.markdown(f"**Source {idx+1}: {src['source']}** (Match Strength: {src['score']:.2f})")
                    st.markdown(f"*{src['text']}*")
                    st.markdown("---")
                    
        # Append to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": retrieved_chunks
        })
        
        # Rerun to refresh scroll placement
        st.rerun()
        
    # Clear conversation history button
    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
