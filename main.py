import time
import os
import pandas as pd
import streamlit as st
import pandas as pd
import functools

from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
)
from llama_index.experimental.query_engine.pandas import (
    PandasInstructionParser,
)
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from llama_index.llms.gemini import Gemini


os.environ["GOOGLE_API_KEY"]= ''
# configuring streamlit page settings
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="💬",
    layout="centered"
)



def retry(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)

        return wrapper
    return decorator

st.title("🤖 Ollama - ChatBot")
uploaded_file=st.file_uploader("Upload your files")
df=pd.DataFrame()
if uploaded_file:
    filetype=(uploaded_file.name).split('.')[-1]
    print("filetype:",filetype)
    if filetype=='csv':
        df=pd.read_csv(uploaded_file)
    elif filetype=='xlsx':
        df = pd.read_excel(uploaded_file)

    print(df)

if df.empty == False:
    # instruction for converting query into executable python code using pandas
    instruction_str = (
        "**Objective:**\n"
        "Translate a natural language query about a Pandas DataFrame into a **concise Python expression**. \n"
        "**Output:**\n"
        "*the columns names of dataframe should match from given list of {columns_str}\n"
        "1. A single-line expression that can be evaluated using the `eval()` function.\n"
        "2. The expression should represent a solution to the given query.\n"
        "3. **Do not include any keywords like 'python' or 'pandas' or any markup language in the expression.**\n"
        "4. Use only necessary Pandas functions and methods.\n\n"
        "**Important Notes:**\n"
        "* The output should be a single line of Python code without any surrounding quotes.\n"
        "* The expression should be concise and efficient.\n"

    )

    # template string for generating a prompt to the language model,including the dataframe and instruction
    pandas_prompt_str = (
        "You are working with a pandas dataframe in Python.\n"
        "The name of the dataframe is `df`.\n"
        "This is the result of `print(df.head())`:\n"
        "{df_str}\n\n"

        "**Important Note:** When dealing with dates in your queries, use `pd.to_datetime()` to convert strings into datetime objects for accurate comparisons and calculations.\n"
        "Follow these instructions strictly:\n"
        "{instruction_str}\n"
        # "remove word python from the expression and then evaluate a expression"
        "Query: {query_str}\n\n"
        "Expression:"
    )

    column_names = "\n".join(f"- {col}" for col in df.columns.tolist())
    print("columns names:",column_names)
    instruction_str = PromptTemplate(instruction_str).partial_format(
        columns_str=column_names
    )
    print("instruction string:",instruction_str)
    pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
        instruction_str=instruction_str, df_str=df.head(5)
    )
    pandas_output_parser = PandasInstructionParser(df)

    llm = Gemini(
        model="models/gemini-1.5-flash",
        # api_key="some key",  # uses GOOGLE_API_KEY env var by default
    )

    qp = QP(
        modules={
            "input": InputComponent(),
            "pandas_prompt": pandas_prompt,
            "llm1": llm,
            "pandas_output_parser": pandas_output_parser,
            # "response_synthesis_prompt": response_synthesis_prompt,
            # "llm2": llm,
        },
        verbose=True,
    )
    qp.add_chain(["input", "pandas_prompt", "llm", "pandas_output_parser"])

    # initialize chat session in streamlit if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []



    # display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # input field for user's message
    user_prompt = st.chat_input("Ask to llama...")

    if user_prompt:
        # add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})


        @retry(max_retries=5, delay=3)
        def call_qp1(querypipelines, user_prompt):
            try:

                response = qp.run(
                    query_str=user_prompt
                )

                # return response.message.content
                print("response:",response)
                if "Error message:" in response:
                    raise Exception
                return response


            except Exception as e:
                print("Exception:", e)
                print("Trying Again 1,2 3....")
                raise

        start_time = time.time()
        response1 = call_qp1(qp, user_prompt)
        print("response 1:",type(response1))


        @retry(max_retries=5, delay=3)
        def call_llm(llm, user_prompt,response1,df):
            try:

                response_synthesis_prompt_str = f'''Convert this question:{user_prompt} answer:{response1}to human redable answer based on question asked
                                                Provide only answer'''

                response = llm.complete(
                    response_synthesis_prompt_str
                )

                # return response.message.content
                print("response:", response)
                if "Error message:" in response:
                    raise Exception
                return response

            except Exception as e:
                print("Exception:", e)
                print("Trying Again 1,2 3....")
                raise

        response2 = call_llm(llm1, user_prompt,response1,df)

        end_time = time.time()
        final_time = end_time - start_time
        print("Final Time:", final_time)
        assistant_response = response2
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        print("output:",response1)

