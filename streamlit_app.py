import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="Repository Research Agent",
    page_icon="🔎",
)


st.title("🔎 Repository Research Agent")

st.write(
    "Ask questions about a GitHub repository and the agent "
    "will automatically use the required GitHub API tools."
)


question = st.text_input(
    "Repository research question",
    placeholder="Analyze facebook/react",
)


if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Researching repository..."):
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60,
                )

            if response.status_code != 200:
                st.error(
                    f"API request failed ({response.status_code}): "
                    f"{response.text}"
                )

            else:
                data = response.json()

                st.subheader("Answer")
                st.markdown(data["answer"])

                tools_used = data.get("tools_used", [])

                if tools_used:
                    st.subheader("Tools Used")

                    for tool in tools_used:
                        st.code(tool)

        except requests.RequestException as exc:
            st.error(f"Could not connect to FastAPI: {exc}")

        except ValueError:
            st.error("FastAPI returned an invalid JSON response.")