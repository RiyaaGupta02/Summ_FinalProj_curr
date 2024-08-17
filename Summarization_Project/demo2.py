import streamlit as sl
# here using sl for streamlit mostly used this helps into development of webapp n sl then used for ref

# trying out here sl and with it all func of streamlit
sl.title("Demo app running")
sl.subheader("learning streamlit basics here")
sl.header("this is the basic header through streamlit")
text_psg = """by this making the text of application basically streamlit made for developing the front-end of the application, using simply python codes"""

sl.markdown(text_psg)     
  #here markdown with the multiline string containing Markdown syntax, including line breaks, the text should be displayed as a passage with multiple lines in the Streamlit visualization. 

# latex helps adding mathematical fun
# sl.latex()

# magic commands
# writes common data science obj that are markdown, number, data frames and chart using variables or values no cmd needed
import pandas as pd
df = pd.DataFrame({'A': [1,2,3], 'B':[4,5,6]})
sl.write(df)
sl.text("what we did here is made a dataframe using simply basic python & streamlit")

sl.text('''so here code appears to create a Pandas DataFrame with 10 rows and 20 columns filled with random numbers drawn from a standard normal distribution using NumPy's random.randn() function
        & then highlighting the max in every col 
        using np for numpy func n pd then as creating table & dataframe''')
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

sl.dataframe(dataframe.style.highlight_max(axis=0))