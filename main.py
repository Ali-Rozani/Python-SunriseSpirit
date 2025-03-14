import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="SunriseSpirit",
    page_icon="🌞",
    layout="centered"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    .stTextInput, .stTextArea {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 10px;
    }
    .mood-response {
        background-color: #f0f7ff;
        border-left: 5px solid #4285f4;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

def initialize_gemini():
    """Initialize and configure the Gemini model"""
    try:
        # Replace with your actual API key
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Configure the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 999999999,
        }
        
        # Initialize Gemini 2.0 Flash model
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config
        )
        
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None

def get_ai_response(user_input, model):
    """Generate a response from the AI model to cheer up the user"""
    try:
        if model is None:
            return "I'm having trouble connecting to my AI brain right now. Please try again later."
        
        # Create a prompt that instructs the model to provide emotional support
        prompt = f"""
        The user is feeling sad or down and has shared the following:
        
        "{user_input}"
        
        Please provide a thoughtful, empathetic, and uplifting response that:
        1. Acknowledges their feelings without dismissing them
        2. Offers genuine encouragement and perspective
        3. Suggests positive actions they might take
        4. Includes a motivational quote or insight if appropriate
        
        Keep your response warm, supportive, and authentic - avoid being overly cheerful 
        in a way that might seem insensitive. Your goal is to help them feel heard and 
        offer gentle support.
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm having trouble generating a helpful response right now. Please try again."

def main():
    """Main application function"""
    # Initialize the model
    model = initialize_gemini()
    
    # App header
    st.markdown("<div class='app-header'>", unsafe_allow_html=True)
    st.title("🌞 SunriseSpirit")
    st.markdown("Share how you're feeling, and let our AI friend lift your spirits")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("How are you feeling today?")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Display thinking spinner while generating response
        with st.spinner("Thinking of something helpful..."):
            ai_response = get_ai_response(user_input, model)
        
        # Add and display AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)
    
    # Additional features section
    with st.expander("More resources to boost your mood"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Quick mood lifters")
            st.markdown("""
            - Take three deep breaths
            - Listen to your favorite upbeat song
            - Step outside for 5 minutes
            - Text a friend who makes you smile
            - Watch a funny video
            """)
        
        with col2:
            st.subheader("Remember")
            st.info("""
            Your feelings are valid, but they aren't permanent.
            Small positive actions can create momentum toward feeling better.
            """)
    
    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("This application is designed to provide emotional support, not to replace professional mental health care.")
    st.markdown("If you're experiencing severe or persistent emotional distress, please reach out to a mental health professional.")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()