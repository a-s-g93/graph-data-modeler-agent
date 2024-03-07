from typing import List
import streamlit as st

def column_input(column_name: str, column_spacing: List[float]) -> None:
    """
    Input component for a column.
    """

    c1, c2, c3 = st.columns(column_spacing)
    with c1:
        use_column = st.checkbox(label="use column", key=column_name+"-use-column-button", label_visibility="collapsed", value=True)
        if not use_column:
            st.session_state["USER_GENERATED_INPUT"].pop(column_name)
    with c2:
        st.text(body=column_name)
    with c3:
        st.session_state["USER_GENERATED_INPUT"][column_name] = st.text_input(label=column_name,
                                    label_visibility="collapsed",
                                    placeholder="column description...")
