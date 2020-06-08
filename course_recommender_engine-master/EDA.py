from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS
import re

from plotly import tools
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go


class Eda():
    
    def generate_ngrams(self, text, n_gram=1):
        if text and isinstance(text, str):
            text = re.sub('\W+', ' ', text)
            token = [token for token in text.lower().split(" ") if token != "" if token not in STOPWORDS]
            ngrams = zip(*[token[i:] for i in range(n_gram)])
            return [" ".join(ngram) for ngram in ngrams]

    def horizontal_bar_chart(self, df, color):
        trace = go.Bar(
            y=df["word"].values[::-1],
            x=df["wordcount"].values[::-1],
            showlegend=False,
            orientation = 'h',
            marker=dict(
                color=color,
            ),
        )
        return trace