import streamlit as st
from openai import OpenAI
from groq import Groq

# Show title and description.
st.title("📄 DoQ&A")
st.write(
    "Upload a document and ask about it – GPT will answer!"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
api_key = st.text_input("[OpenAI](https://platform.openai.com/account/api-keys)/[Grok](https://x.ai/api) API key.", type="password")
if not api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    if not api_key.startswith("xai"):
        model = "gpt-4o-mini"
        # Create an OpenAI client.
        client = OpenAI(api_key=api_key)
    else:
        # Create an Grok client.
        client = Groq(api_key=api_key)
        model = "rok-2-latest"


    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Questions about the document:",
        value="Give me a short summary with ordered lists.",
        disabled=not uploaded_file,
    )

    # Add a submit button
    if st.button("Submit"):
        # Process the text when the button is clicked
        if question:
            if uploaded_file and question:

                # Process the uploaded file and question.
                document = uploaded_file.read().decode('utf-8-sig', 'ignore')
                messages = [
                    {
                        "role": "system",
                        "content": "You are a Document Analyst, specialized in processing diverse document types. Your role is to provide short, clear summaries in visually structured formats. Use Markdown for formatting, focus on key information, and suggest where visual aids might help understanding."
                    },{
                        "role": "user",
                        "content": f"Here's a document: {document} \n\n---\n\n {question}",
                    }
                ]

                # Generate an answer using the OpenAI API.
                stream = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                    store=False,
                )

                # Stream the response to the app using `st.write_stream`.
                st.write_stream(stream)
        else:
            st.warning('Enter some text before submitting.', icon="⚠️")