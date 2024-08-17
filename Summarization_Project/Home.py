import streamlit as sl
from PIL import Image
import numpy as np

# making a heading sub title and then sidebar
# initialize the pg
sl.set_page_config(
    page_title= "Summarization_Site",   # Then use the set_page_config() method of Streamlit to provide a page_title of that page
    page_icon= ":memo:", 
   )

home_text = """ Unleash text's power: Summarize your text, url, pdf and visualizing your csv file. Also refine with research (Curious Assistant!), and stay tuned for a document chatbot (coming soon!).
                For upcoming features visit About Us"""
with sl.sidebar:
    sl.text_area("Brief", value=home_text, height= 130)           #here disabled being true makes the text-box uneditable & secures it


sl.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)
# heading 
sl.markdown("""
<h1>
    <i class="fa-solid fa-pen-to-square"></i>
    <span style="color: #281862; opacity: 1; font-size: 1.5em;">SwiftRead</span>
</h1>
""", unsafe_allow_html=True)
sl.subheader("Summarization Essentials")

intro_emoji = "Message :smile: "
intro_text = """For an effective summarization, understanding its principles is crucial. It involves condensing content to its vital points for clarity and brevity.
For refrence can observe below present demos on how our site works."""
sl.text_area(intro_emoji, value=intro_text,height=120)

#Importing an image to show
# Load image using PIL
image = Image.open('Summarize.jpg')

# Convert PIL image to numpy array
img_array = np.array(image)
# Allow the user to specify the desired width of the image using a slider
desired_width = sl.slider("For zooming into image:", min_value= 500, max_value= 900, value=500, step=10)

sl.text("Summarisation for text may look like this:")
sl.image(img_array, width= desired_width)

img2 = Image.open('PdfSummpic.jpg')
# Convert PIL image to numpy array
img_array = np.array(img2)
sl.text("Summarisation for PDF may look like this:")
sl.image(img_array, width= desired_width)

img_Curious = Image.open('Cur_Ask2.jpeg')
# Convert PIL image to numpy array
img_array = np.array(img_Curious)
sl.text("A look on how Curious Ask chatbot functions")
sl.image(img_array, width= desired_width)