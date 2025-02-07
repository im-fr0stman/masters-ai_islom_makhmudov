import streamlit as st
import datetime
from assistant import analyze_question
from functions import fetch_external_data


def main():
    """Streamlit UI"""
    st.set_page_config(page_title="AI Data Assistant", page_icon="🌍", layout="wide")

    # Custom Styling
    st.markdown(
        """
        <style>
            .title-text {
                font-size: 36px;
                font-weight: bold;
                color: white;
            }
            .subtitle-text {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            .description-text {
                font-size: 18px;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""<h1 class='title-text'>🌍 AI Data Assistant</h1>""", unsafe_allow_html=True)
    st.markdown(
        """<p class='description-text'>This AI Assistant can answer questions related to the Countries database and general queries.</p>""",
        unsafe_allow_html=True)

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "External Data", "Settings"])

    if page == "Chat":
        st.text_input("Enter your name:")
        st.text_input("Enter your email:")
        send_email = st.checkbox("Send response to email")

        user_input = st.text_area("Enter your query:")
        if st.button("Submit"):
            if user_input:
                response = analyze_question(user_input)
                st.subheader("Response:")
                st.write(response)

                if send_email:
                    st.success("Response will be sent to your email.")
            else:
                st.warning("Please enter a query.")

    elif page == "External Data":
        st.header("Fetch External Data")
        query = st.text_input("Enter search term:")
        if st.button("Fetch Data"):
            if query:
                data = fetch_external_data({"query": query})
                st.subheader("API Response:")
                st.json(data)
            else:
                st.warning("Please enter a search term.")

    elif page == "Settings":
        st.header("Settings")
        theme = st.radio("Select Theme", ["Light", "Dark"])
        st.write(f"Selected Theme: {theme}")


if __name__ == "__main__":
    main()
