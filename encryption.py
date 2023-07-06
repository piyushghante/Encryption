from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import math
import os
from PIL import Image
import os
import streamlit as st
import webbrowser

st.set_page_config(
    page_title="UI1",
    page_icon="🥵",
    layout="centered",
)

key=b'\xbf\x1b\xb3O\x8fB\x88e\x04\xea\xfb\xcd{.\xa9\xdc<\xef\xeb\xb9\x08\x10\xd3\x18\x92\x0f\xb6\x80\xe1 <V'


def data_to_image(data, image_path):
    binary_data = "".join(format(byte, "08b") for byte in data)
    data_len = len(binary_data)
    img_width = int(math.sqrt(data_len)) + 1
    img_height = int(math.ceil(data_len / img_width))
    img = Image.new("L", (img_width, img_height), color=255)
    for i, bit in enumerate(binary_data):
        x = i % img_width
        y = i // img_width
        pixel_value = 255 - int(bit) * 255
        img.putpixel((x, y), pixel_value)
    img.save(image_path)

st.title("Encrypt File")

# Upload the original image file
original_file = st.file_uploader("Upload the originalfile", type=["docx",  "pdf",  "jpg","jpeg",  "png",  "gif",  "mp3",  "mp4",  "avi",  "zip",  "rar",  "pptx",  "xlsx",  "html",  "css",  "js",  "php",  "exe",  "dll",  "txt",  "rtf"])
if original_file:
    # Save the original image data to a variable
    original_data = original_file.read()

    # Get the file extension from the original file name
    original_file_ext = os.path.splitext(original_file.name)[1]

    # Reserve space for the file extension in the binary data
    header_size = 4 # bytes
    extension_size = len(original_file_ext)
    reserved_data_size = header_size + extension_size
    binary_data = bytearray(reserved_data_size + len(original_data))

    # Add the file extension to the header
    binary_data[:header_size] = extension_size.to_bytes(header_size, byteorder='big')
    binary_data[header_size:header_size+extension_size] = original_file_ext.encode("utf-8")

    # Add the original file data to the binary data
    binary_data[reserved_data_size:] = original_data

    # Convert the binary data to a binary string
    binary_string = "".join(format(byte, "08b") for byte in binary_data)

    # Write the binary string to a TXT file
    with open("example.txt", "w") as f:
        f.write(binary_string)

    # Read the message from the text file
    with open('example.txt', 'rb') as f:
        message = f.read()

    # Generate a random 16-byte initialization vector (IV)
    iv= b'P\x05\x95\xac\xf5\x88\x9c\x1a\x89\x94 ^\x92i\xc8\xbc'

    # Generate a random 32-byte key
    key2= get_random_bytes(32)
    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CFB, iv)

    # Pad the message so that its length is a multiple of 16
    padded_message = pad(message, AES.block_size,style='pkcs7')

    # Encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message)

    # Convert the encrypted message to an image and save it
    data_to_image(encrypted_message, 'encrypted_image.png')

    # Display the encrypted image
    encrypted_image = Image.open('encrypted_image.png')
    st.image(encrypted_image)

    # Add a


    # Add a button to download the encrypted image
def download_file(file_path, file_name):
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    st.download_button(label="Download", data=file_bytes, file_name=file_name)

st.subheader('Key')
st.code(key)




#st.image('encrypted_image.png', caption='Encrypted Image')

# Add a button to download the encrypted image
download_file('encrypted_image.png', 'encrypted_image.png')
phone_number=st.text_input("Enter Whatsapp Number")

whatsapp_url = f"https://api.whatsapp.com/send/?phone={phone_number}&text={key}&type=phone_number&app_absent=1"
def open_url():
    webbrowser.open_new_tab(whatsapp_url)
if st.button('Send Key to Whatsapp'):
    open_url()


margin='50px'

st.write(f'<div style="margin: {margin}"></div>', unsafe_allow_html=True)

st.write('Steps to be followed to Encrypt File')
video='env.webm'
st.video(video)
