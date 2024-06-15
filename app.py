import streamlit as st
from langchain.llms import CTransformers
import re

# Load the Llama 2-7b model
model = CTransformers(model='llama-2-7b-chat.ggmlv3.q8_0.bin', model_type='llama', allow_reuse=True)

def generate_content(topic, max_length=1000):
    # Prepare the prompt for content generation
    prompt = f"Generate the best solutions and advice to the problem in the topic: {topic}\n\n"
    
    # Generate the content
    generated_content = model.predict(prompt, max_length=max_length, stop=None)
    
    # Split the generated content into pages
    pages = re.split(r"\n{2,}Page \d+\n{2,}", generated_content)
    
    return pages

def download_text(text):
    with open("generated_solutions.txt", "w", encoding="utf-8") as file:
        file.write(text)
    
    with open("generated_solutions.txt", "rb") as file:
        st.download_button(
            label="Download Generated Solutions",
            data=file,
            file_name="generated_solutions.txt",
            mime="text/plain"
        )

def main():
    st.title("AI Solutions for Mental Well-being")
    st.write("Enter a input the feelings and problems you are facing and let the AI generate solutions")
    
    # Get user input for the topic
    topic = st.text_input("Enter a problem:")
    
    if st.button("Generate Solutions"):
        if topic:
            # Generate the content
            pages = generate_content(topic)
            
            # Display the generated content
            st.subheader("Generated Solutions")
            for i, page_content in enumerate(pages, start=1):
                st.write(f"### Page {i}")
                st.write(page_content)
                st.write("---")
            
            # Download the generated content as a text file
            download_text("\n".join(pages))
        else:
            st.warning("Please enter a topic to generate solutions.")

if __name__ == "__main__":
    main()