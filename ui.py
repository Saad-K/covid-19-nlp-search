import requests
import streamlit as st


"""
# COVID-19 Natural Language Search

Applying Semantic Natural Language Search using BERT to the 50,000 COVID research papers published.
The goal is to help researchers fighting this in the field quickly identify needed information.
"""

init_results = [
    {
        "score": "0.7080",
        "set_of_sentences": "while augmented intelligence ai in healthcare has been widely cited as an important approach to aid in the detection of disease and making clinical diagnosis this recent outbreak emphasizes the need and opportunity to utilize ai to predict outbreaks while the use of expert epidemiologists and public health officials cannot be replaced ai can serve to compile rapidly evolving information to assist public health experts in complex decisionmaking aggregation of social media news media rapidly evolving health reports and other disparate data is a daunting task which ai is poised to overcome during prior outbreaks such as severe acute respiratory syndrome sars in china in 2003 little realtime data was available [5] now there is an explosion of available data and the tools utilized presently must meet that and overcome the challenge of big data",
        "paper_id": "8b4a52e7b0b63c560fa7856df220f40ded79b10f",
        "title": " The Role of Augmented Intelligence (AI) in<br>Detecting and Preventing the Spread of Novel Coronavirus",
        "abstract": "nan",
        "abstract_summary": "Not provided",
    }
]

status = st.empty()

@st.cache()
def fetch_results(question):
    """
    Infer results of questions from the model.
    """
    with st.spinner("Waiting for inference results..."):
        r = requests.post("http://localhost:8000/predict", json=question)
        results = r.json()
    status.success("Done!")

    return results


question = st.text_input(
    "Question:",
    value="Use of AI in real-time health care delivery to evaluate interventions, risk factors, and outcomes in a way that could not be done manually",
)

submit = st.button("Submit")

results = fetch_results([question]) if submit else init_results


st.subheader("Results:")

result_text = st.empty()
mark = ""
for item in results:
    mark += f"""
        ---
        **Title:** { item['title'] }

        **Paper ID:** { item['paper_id'] }

        **Score:** { item['score'] }

        **Set of Sentences:** { item['set_of_sentences'] }

        **Abstract:** { item['abstract'] }

        **Abstract Summary:** { item['abstract_summary'] }
        """

mark  # %% [markdown]
