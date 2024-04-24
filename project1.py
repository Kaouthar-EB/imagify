import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64

custom_css = """
    <style>
        [data-testid="stAppViewContainer"] section {
        background-color: #000
        }
        [data-testid='stHeader']  {
        color:rgb(100 100 100);
        background-color: #1d1d1d
        }
        [data-testid='stFileUploader'] section {
        background-color:rgb(10 10 10)
        }
        [data-testid='stFileUploader'] section span {
        color: #fff
        }
        [data-testid='stFileUploader'] section small {
        color: #4e737d
        }
        [data-testid='stFileUploader'] section button {
        border-color: #fe0000 !important;
        color: #fe0000 !important;
        }
        [data-testid='stFileUploader'] section button:hover {
        border-color: #fe0000 !important;
        color: #fff!important;
        background-color: #fe0000
        }
        [data-testid='stFileUploaderDeleteBtn'] button:hover {
        color: #fe0000!important;
        }
        [data-testid='stMarkdownContainer'] h6 {
        text-align: center;
        }

        [data-testid='stThumbValue'] {
        color: #fe0000!important;
        }
        [role='slider'] {
        background-color: #fe0000 !important;
        }

        [class='st-dg st-cv st-cx st-cw st-af st-dh st-di'] div:first-child(){
            background-color: #fe0000 !important;
        }

        [data-baseweb="checkbox"] span::before {
    background-color: #fe0000 !important;

        [data-baseweb="checkbox"] span{
            border-color: #fe0000 !important;
        }
        .stCheckbox input:checked + span::before {
    background-color: #fe0000 !important;
}
        
        /* Checkbox style */
        input[type="checkbox"] {
            opacity: 1 !important;
        }
    
    </style>
"""

def get_image_download_link(img_bytes, filename, text):
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/jpeg;base64,{b64}" download="{filename}">{text}</a>'
    return href

st.set_page_config(page_title="Imagify", page_icon="./icon.png", layout="centered", initial_sidebar_state="collapsed")
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown("""<style> [data-testid = "stAppViewContainer"]{background-color: black;} </style>""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 10px #fe0000; font-size: 70px'>Imagify</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color:#fff; text-shadow: 1px 1px 5px #fe0000; font-size: 15px;'>---modify your image---</h1>", unsafe_allow_html=True)

image = st.file_uploader("Upload Your Image", type=["jpg", "png", "jpeg"])
if image:
    img = Image.open(image)
    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Information</h1>", unsafe_allow_html=True)
    st.markdown(f"<h6>Mode: {img.mode}</h6>", unsafe_allow_html=True)
    st.markdown(f"<h6>Format: {img.format}</h6>", unsafe_allow_html=True)
    st.markdown(f"<h6>Size: {img.size}</h6>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Resize</h1>", unsafe_allow_html=True)
    width = st.number_input("Width", value=img.width)
    height = st.number_input("Height", value=img.height)

    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Rotation</h1>", unsafe_allow_html=True)
    degree = st.number_input("Rotation Degree", 0.0, 360.0, 0.0, 0.01)

    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Filters</h1>", unsafe_allow_html=True)
    filter = st.selectbox("Filter", options=["None", "Blur", "Emboss", "Smooth", "Detail", "Contour", "Sharpen"])

    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Modifications</h1>", unsafe_allow_html=True)
    brightness = st.slider("Brightness", -100, 100, 0)
    contrast = st.slider("Contrast", -100, 100, 0)

    red_checkbox = st.checkbox("Red")
    green_checkbox = st.checkbox("Green")
    blue_checkbox = st.checkbox("Blue")
    grayscale_checkbox = st.checkbox("Grayscale")
    transpose_checkbox = st.checkbox("Transpose")
    st.markdown("<h1 style='text-align: center; color:#fe0000; text-shadow: 1px 1px 5px #fe0000; font-size: 30px'>Superpose Image</h1>", unsafe_allow_html=True)
    second_image = st.file_uploader("Upload Second Image (Optional)", type=["jpg", "png", "jpeg"])

    # Select overlay position
    overlay_position = (st.number_input("Overlay Position X", value=0), st.number_input("Overlay Position Y", value=0))

    # Checkboxes to select overlay options
    overlay_options = st.checkbox("Apply Overlay", value=False)


    submit = st.button("Submit")
    if submit:
        new_img = img.resize((width, height)).rotate(degree)
        if filter != "None":
            if filter == "Blur":
                new_img = new_img.filter(ImageFilter.BLUR)
            elif filter == "Emboss":
                new_img = new_img.filter(ImageFilter.EMBOSS)
            elif filter == "Smooth":
                new_img = new_img.filter(ImageFilter.SMOOTH)
            elif filter == "Detail":
                new_img = new_img.filter(ImageFilter.DETAIL)
            elif filter == "Contour":
                new_img = new_img.filter(ImageFilter.CONTOUR)
            elif filter == "Sharpen":
                new_img = new_img.filter(ImageFilter.SHARPEN)

        brightness_enhancer = ImageEnhance.Brightness(new_img)
        new_img = brightness_enhancer.enhance((brightness + 100) / 100)

        contrast_enhancer = ImageEnhance.Contrast(new_img)
        new_img = contrast_enhancer.enhance((contrast + 100) / 100)
        
        if overlay_options and second_image:
            with Image.open(second_image) as overlay_img:
                
                overlay_img.load()
                new_img.paste(overlay_img, overlay_position)


        zeroed_band = new_img.split()[0].point(lambda _: 0)  # Create a zeroed band
        if red_checkbox:
            red_merge = Image.merge("RGB", (new_img.split()[0], zeroed_band, zeroed_band))
            new_img = red_merge

        if green_checkbox:
            green_merge = Image.merge("RGB", (zeroed_band, new_img.split()[1], zeroed_band))
            new_img = green_merge

        if blue_checkbox:
            blue_merge = Image.merge("RGB", (zeroed_band, zeroed_band, new_img.split()[2]))
            new_img = blue_merge

        if grayscale_checkbox:
            new_img = new_img.convert("L")


        if grayscale_checkbox:
            new_img = new_img.convert("L")
        
        if transpose_checkbox:
            new_img = new_img.transpose(Image.FLIP_TOP_BOTTOM)
            
        st.image(image, caption='Modified Image', use_column_width=True)
        st.image(new_img, caption='Modified Image', use_column_width=True)

        # Convert the image to RGB mode if it's RGBA
        if new_img.mode == "RGBA":
            new_img = new_img.convert("RGB")
        # Save the image to BytesIO buffer
        img_byte_arr = io.BytesIO()
        new_img.save(img_byte_arr, format='JPEG')
        # Display the link for downloading
        st.markdown(get_image_download_link(img_byte_arr.getvalue(), filename="modified_image.jpg", text="Download Image"), unsafe_allow_html=True)
