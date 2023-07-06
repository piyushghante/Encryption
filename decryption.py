from Crypto.Cipher import AES
from key import key as key1
from Crypto.Util.Padding import pad
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Decryption",
    page_icon="🥶",
    layout="centered",
)
st.title("Decrypt File")


key=b'\xbf\x1b\xb3O\x8fB\x88e\x04\xea\xfb\xcd{.\xa9\xdc<\xef\xeb\xb9\x08\x10\xd3\x18\x92\x0f\xb6\x80\xe1 <V'

def image_to_data(image_path):
    img = Image.open(image_path).convert("L")
    width, height = img.size
    binary_str = ""
    for i in range(height):
        for j in range(width):
            pixel_value = img.getpixel((j, i))
            binary_str += "1" if pixel_value < 128 else "0"
    binary_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
    return binary_data


def decrypt_image(encrypted_image_path, key, iv, output_file_path):
    # Read the encrypted message from the image
    encrypted_message = image_to_data(encrypted_image_path)

    # Create an AES cipher object with the key and IV
    cipher = AES.new(key,AES.MODE_CFB, iv)

    # Decrypt the encrypted message
    decrypted_message = cipher.decrypt(encrypted_message)

    # Unpad the decrypted message
    unpadded_message = pad(decrypted_message, AES.block_size)

    # Write the decrypted message to a text file
    with open(output_file_path, 'wb') as f:
        f.write(unpadded_message)
# Read the key and IV used for encryption
key2=st.text_input("Enter Key")
iv = b'P\x05\x95\xac\xf5\x88\x9c\x1a\x89\x94 ^\x92i\xc8\xbc'

# Decrypt the message from the image and write it to a text file
output_file_path = 'Cell6.txt'

print(f"Decrypted data written to {output_file_path}")

# Open the input and output files
with open("Cell6.txt", "r") as input_file, open("process.txt", "w") as output_file:
    # Read the contents of the input file
    input_str = input_file.read()

    # Remove any characters other than 0 and 1
    filtered_str = ''.join(c for c in input_str if c in {'0', '1'})

    # Write the filtered string to the output file
    output_file.write(filtered_str)


# Define the path and name of the binary TXT file
binary_file_path = "process.txt"

# Read the binary string from the TXT file
with open(binary_file_path, "r") as f:
    binary_string = f.read()

# Convert the binary string to binary data
binary_data = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))

# Get the file extension from the binary data header
header_size = 4 # bytes
extension_size = int.from_bytes(binary_data[:header_size], byteorder='big')
original_file_ext = binary_data[header_size:header_size+extension_size].decode("utf-8")

# Extract the original file data from the binary data
original_data = binary_data[header_size+extension_size:]

# Write the original file with the correct file extension
with open("example3" + original_file_ext, "wb") as f:
    f.write(original_data)  



# Set up the drag and drop box
uploaded_file = st.file_uploader("Drag and drop an image here", type=["jpg", "jpeg", "png"])

# Check if a file has been uploaded
if uploaded_file is not None:
    decrypt_image(uploaded_file, key, iv, output_file_path)
else:
    # Prompt the user to upload a file
    st.write("Drag and drop an image file to decrypt.")


file="example3."+original_file_ext
# Define a function that returns the content of the file as a byte string
def get_file_content_as_string(file):
    content = file.read()
    return content

# Define the Streamlit app
def app():  
    


   
    # Add a download button
       
        
        st.download_button(
           label="Download Processed File",
    data=bytes(original_data),
    file_name=file,
    mime="text/plain"
            
        )

if __name__ == "__main__":
    app()
