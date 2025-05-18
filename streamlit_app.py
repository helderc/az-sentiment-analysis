import streamlit as st
import pandas as pd
from collections import Counter

from AzSentimentAnalysis import AzSentimentAnalysis

def infer_sentiment(text: list): 
    clt = AzSentimentAnalysis().get_conn()

    documents = [{"id": str(i), "language": "en", "text": t} for i, t in enumerate(text)]
    response = clt.analyze_sentiment(documents=documents)
    res = {"sentence":[], "sentiment":[], "confidence":[]}
    for r in response:
        if not r.is_error:
            idx = int(r.id)
            original_text = text[idx]
            res["sentence"].append(original_text)
            res["sentiment"].append(r.sentiment)
            res["confidence"].append(dict(r.confidence_scores))
        else:
            print(f"Error analyzing sentiment for ID {r.id}: {r.error}")
    return res


with st.columns(3)[1]:
    st.image("img/sentiment-analysis-app.jpg")

st.header("Sentiment Analysis App")

st.markdown("---")
st.markdown("**Check the repository of this project on GitHub: https://github.com/helderc/az-sentiment-analysis**")
    #("", icon="👨‍🏫")
st.error('''
         If you see error "azure.core.exceptions.ServiceRequestError" it means that
         the Azure AI Cognitive Service was disabled to stay within the free tier.''', 
        icon="⚠️")
st.markdown("---")

text_area = st.text_area("Enter text (or copy one or more lines from the sample data:", height=200)

with st.expander("Sample data"):
    st.write('''
        I really enjoyed the course. The content was well-structured, and the instructor explained everything clearly.\n
        The course exceeded my expectations. The topics were relevant, and I appreciated the practical examples.\n
        It was one of the best courses I've taken. I felt constantly engaged and supported.\n
        The course content was good, but sometimes the pace was a bit fast for me.\n
        I think the materials are okay, but the delivery could be a bit more interactive.\n
        Some topics were interesting, while others felt a bit rushed. Overall, it was decent.\n
        I found the course confusing at times. It would help to have more real-world examples.\n
        The content felt outdated and the lectures were hard to follow.\n
        Honestly, I struggled to stay engaged. The delivery style didn't work well for me.\n
        The course didn't meet my expectations. I felt lost in most of the sessions.\n
    ''')

if st.button("Analyze"):
    lines = [line.strip() for line in text_area.strip().split("\n") if line.strip()]

    result = infer_sentiment(lines)
    df_log = pd.DataFrame(result)
    
    st.subheader("Sentiments")
    counts = Counter(result["sentiment"])
    df = pd.DataFrame.from_dict(counts, orient='index', columns=['Count'])
    st.bar_chart(df)

    st.subheader("Weighted Confidence by Sentiment")
    df = pd.DataFrame(df_log)

    df['positive_confidence'] = df['confidence'].apply(lambda x: x['positive'])
    df['neutral_confidence'] = df['confidence'].apply(lambda x: x['neutral'])
    df['negative_confidence'] = df['confidence'].apply(lambda x: x['negative'])

    weighted_confidence = df.groupby('sentiment')[
        ['positive_confidence', 'neutral_confidence', 'negative_confidence']
    ].sum().reset_index()

    st.bar_chart(weighted_confidence.set_index("sentiment"))

    st.subheader("Log")
    st.table(df_log)