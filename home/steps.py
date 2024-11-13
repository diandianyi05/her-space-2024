import streamlit as st
from home.prompts import build_empowerment_prompt
import google.generativeai as genai
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from resource_page.safe_hub import crisis_support_resources
from home.utils import get_api_key


# At the top of steps.py, make sure all functions are listed in __all__
__all__ = [
    'render_welcome_step',
    'render_thoughts_step',
    'render_emotions_step',
    'render_support_step',
    'render_strengths_step',
    'render_goals_step',
    'render_final_step',
    'render_summary_step',
    'render_response_step'
]

# Initialize session states
def init_session_state():
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    if "custom_thoughts_list" not in st.session_state:
        st.session_state.custom_thoughts_list = []
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    if "custom_emotions_list" not in st.session_state:
        st.session_state.custom_emotions_list = []
    if "custom_strengths_list" not in st.session_state:
        st.session_state.custom_strengths_list = []
    if "custom_support_list" not in st.session_state:
        st.session_state.custom_support_list = []

def next_step():
    if 'gemini_api_key' not in st.session_state or not st.session_state.gemini_api_key:
        st.error("Please configure your Gemini API key first.")
        return  # Prevent moving to next step
    st.session_state.current_step += 1

def prev_step():
    st.session_state.current_step -= 1

def delete_thought(index):
    st.session_state.custom_thoughts_list.pop(index)
    st.rerun()

def render_welcome_step():
    """Render the welcome step (Step 1) of the form."""
    st.divider()
    # Initialize session state for form data if it doesn't exist
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "situation": "",
            "category": "",
            "thoughts": "",
            "emotions": "",
            "support_system": "",
            "strengths": "",
            "goal": "",
            "extra_notes": ""
        }

    st.markdown(
        '<div class="fade-in step-1">'
        '<p class="section-title">✨ Welcome to Your AI-Powered Safe Space ✨</p>'
        '<p>Here, we understand. This platform is all about supporting women with smart, AI-powered solutions. It’s a safe space to talk about the real challenges and questions in life. Whatever you\'re going through, we\'re here to help—you\'re not alone in this.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()
    get_api_key()

    st.divider()

    # Define options list
    category_options = [
        "Select an topic...",
        "Women in Leadership & Glass Ceiling",
        "Gender Inequality in Education",
        "Workplace Gender Discrimination",
        "Pregnancy & Parenting Challenges",
        "Domestic Violence",
        "Work-Life Balance Struggles",
        "Body Image & Beauty Standards",
        "Online Harassment & Cyberstalking",
        "Offline Harassment",
        "Unhealthy Relationships",
        "Other (please specify)"
    ]
    # Get the current category from session state
    current_category = st.session_state.form_data.get("category", "Select an topic...")

    # Check if the current category exists in category_options
    if current_category in category_options:
        index = category_options.index(current_category)
    else:
        index = category_options.index("Other (please specify)")

    # Get user input with previous value
    concern_category = st.selectbox(
        "Which topic would you like to focus on?",
        category_options,
        index=index
    )

    # Show situation input if category is selected
    proceed_to_next = False
    if concern_category != "Select an topic...":
        # Check if the user selected "Other (please specify)"
        if concern_category == "Other (please specify)":
            # Check if a custom category has already been entered
            if "custom_category" not in st.session_state:
                st.session_state.custom_category = ""  # Initialize if not present

            # Display the text input for custom category
            custom_category = st.text_input("Please specify your category:", value=st.session_state.custom_category)

            # Update session state with the custom category input
            st.session_state.custom_category = custom_category

            # Update form data with custom category if provided
            st.session_state.form_data["category"] = custom_category if custom_category else concern_category
        else:
            # Update form data with the selected category
            st.session_state.form_data["category"] = concern_category

        situation = st.text_area(
            "Could you tell me more about what's happening?",
            value=st.session_state.form_data.get("situation", ""),  # Load previous situation
            help="Share as much as you feel comfortable with. You can also explore \"Crisis Support Resources\" and \"Therapy Location Finder\" pages on this site if you need help.",
            placeholder="For example: 'I'm feeling overwhelmed with...'\nPlease try to share your thoughts and feelings in as much detail as possible.\nThe information will be saved automatically when you press 'Next'."
        )
        
        # Update form data with the situation
        st.session_state.form_data["situation"] = situation

        # Create two columns for the buttons
        col1, col2 = st.columns([8, 1])
        gif_path = get_gif_path(st.session_state.current_step)
        step_name = "situation"

        with col1:
            display_agent_section(step_name, gif_path, "user described their situation and concern_category now, discuss the situation with the user")
        with col2:
            if st.button("Next", on_click=next_step):
                proceed_to_next = True

        return proceed_to_next

def render_thoughts_step():
    init_session_state()  # Call at the start of first step
    st.divider()
    st.markdown('<p class="section-title">💭 Understanding Your Thoughts</p>', unsafe_allow_html=True)
    
    predefined_thoughts = [
        "I'm not good enough", "I should be doing better",
        "Others are judging me", "I can't handle this",
        "This is too difficult", "I'll never succeed",
        "I deserve better", "I can learn from this",
        "This is temporary"
    ]

    # Initialize thoughts list in session state if not exists
    if "selected_thoughts" not in st.session_state:
        st.session_state.selected_thoughts = []

    # Display predefined thoughts as clickable buttons
    st.markdown("##### Select thoughts that resonate with you:")
    
    # Create rows of buttons for predefined thoughts
    cols = st.columns(3)  # Adjust number of columns as needed
    for i, thought in enumerate(predefined_thoughts):
        with cols[i % 3]:
            # Check if thought is already selected
            is_selected = thought in st.session_state.selected_thoughts
            button_type = "primary" if is_selected else "secondary"
            
            if st.button(
                thought, 
                key=f"thought_{i}",
                type=button_type,
                help="Click to select/deselect this thought"
            ):
                if is_selected:
                    st.session_state.selected_thoughts.remove(thought)
                else:
                    st.session_state.selected_thoughts.append(thought)
                st.rerun()

    # Custom thoughts section
    st.markdown("##### 💭 Or share your own thoughts:")
    
    # Display existing custom thoughts with delete buttons
    for i, thought in enumerate(st.session_state.custom_thoughts_list):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f'<div class="custom-thought-box">'
                      f'<span class="thought-text">{thought}</span>'
                      f'</div>', 
                      unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"delete_custom_{i}", help="Delete this thought"):
                delete_thought(i)
    def add_and_clear():
        if st.session_state.new_thought_input.strip():  # Only add non-empty thoughts
            add_item(st.session_state.new_thought_input, st.session_state.custom_thoughts_list)
            st.session_state.new_thought_input = ""

    step_name = "thoughts"
    gif_path = get_gif_path(st.session_state.current_step)
    # Add new thought
    col1, col2 = st.columns([8, 1])

    with col1:
        st.text_input(
            "Add your thought here:",
            placeholder="Enter your thought...",
            key="new_thought_input",
            label_visibility="collapsed",
            help="",
            on_change=add_and_clear
        )
    with col2:
        st.button("Add", 
                 type="primary", 
                 key="add_thought_button",
                 on_click=add_and_clear)

    # Update form_data with all thoughts (selected + custom)
    st.session_state.form_data["thoughts"] = st.session_state.selected_thoughts + st.session_state.custom_thoughts_list

    # Add vertical spacing
    st.write("")
    st.write("")

    # Navigation buttons
    col5, col3, col4 = st.columns([8, 1, 1]) 

    with col3:
        st.button("Back", on_click=prev_step)
    with col4:
        st.session_state.form_data[step_name].extend(st.session_state.custom_thoughts_list)
        st.button("Next", on_click=next_step)
    with col5:
        display_agent_section(step_name, gif_path, "user has shared their thoughts now, discuss the thoughts with the user")

def add_item(new_item, item_list, just_added_key=None):
    """Generic function to add items to a list in session state
    
    Args:
        new_item: The item to add
        item_list: The list to add to (from session state)
        just_added_key: Optional key to set in session state for tracking latest addition
    """
    if new_item and new_item not in item_list:
        item_list.append(new_item)
        if just_added_key:
            st.session_state[just_added_key] = True

def delete_item(index: int, list_key: str):
    """
    Generic function to delete an item from a list in session state.
    
    Args:
        index: Index of item to delete
        list_key: The session state key for the list
    """
    st.session_state[list_key].pop(index)
    st.rerun()

def render_emotions_step():
    st.divider()
    st.markdown('<p class="section-title">💗 Your Emotions</p>', unsafe_allow_html=True)
    
    # Combine default and custom emotions for selection
    default_emotions = ["😔 Sad", "😠 Angry", "😟 Anxious", "😊 Hopeful", "😕 Confused", "Other..."]
    
    # Primary emotion selection
    primary_emotion = st.selectbox(
        "Primary emotion:",
        default_emotions,
        index=len(default_emotions)-1 if st.session_state.get("show_custom", False) else 0
    )
    
    # Show custom input if "Other..." is selected
    if primary_emotion == "Other...":
        st.session_state.show_custom = True
        st.info("💡 You can add emojis to express your emotion better. For example: 😌 Peaceful, 🤗 Grateful, 😤 Frustrated")
        custom_emotion = st.text_input(
            "",
            placeholder="Example: 😌 Peaceful",
            key="custom_emotion",
            label_visibility="collapsed"
        )
        if custom_emotion:
            primary_emotion = custom_emotion
    else:
        st.session_state.show_custom = False
    
    # Constants
    INTENSITY_OPTIONS = ["\nMild\n", "\nModerate\n", "\nStrong\n", "\nVery Strong\n"]
    DEFAULT_INTENSITY = INTENSITY_OPTIONS[0]

    # Intensity selection
    intensity = st.select_slider(
        "How intense is this feeling?",
        options=INTENSITY_OPTIONS,
        value=st.session_state.form_data.get("emotion_intensity", DEFAULT_INTENSITY)  # Use consistent key
    )
    
    # Update form data
    st.session_state.form_data.update({
        "primary_emotion": primary_emotion,
        "emotion_intensity": intensity 
    })
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    step_name = "emotions"
    gif_path = get_gif_path(st.session_state.current_step)
    
    # Navigation buttons and agent support
    col_agent, col_back, col_next = st.columns([8, 1, 1])
    
    with col_back:
        st.button("Back", on_click=prev_step)
    
    with col_next:
        st.button("Next", on_click=next_step)
        
    with col_agent:
        display_agent_section(step_name, gif_path, "user has shared their emotions now, discuss the emotions with the user")

def render_support_step():
    st.divider()
    step_name = "support_system"
    st.markdown('<p class="section-title">👥 Positive Thinking: Your Support Network</p>', unsafe_allow_html=True)
    # Initialize form data for support if not exists
    if step_name not in st.session_state.form_data:
        st.session_state.form_data[step_name] = ""
    support = st.multiselect(
        "Who can you reach out to for support?",
        ["Family members", "Close friends", "Professional help",
         "Support groups", "Mentor", "Spiritual/Religious community",
         "None currently"]
    )

    # Convert selected support to string
    selected_support = ", ".join(support) if support else ""
    st.session_state.form_data[step_name] = selected_support
    # Show supportive message if "None currently" is selected
    if "None currently" in support:
        st.info("💫 Remember, you're not alone in this journey. Our platform provides a safe space for you to express yourself and find guidance. You can also explore the \"Crisis Support Resources\" and \"Therapy Location Finder\" pages on this site if you need help.")
    # Custom support section
    st.markdown("##### 👥 Or add other support sources:")
    # Display existing support sources with delete buttons
    for i, support_item in enumerate(st.session_state.custom_support_list):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f'<div class="custom-thought-box">'
                      f'<span class="thought-text">{support_item}</span>'
                      f'</div>', 
                      unsafe_allow_html=True)
        with col2:
            st.write("")  # Add spacing to align with text
            if st.button("🗑️", key=f"delete_support_{i}", help="Delete this support source"):
                delete_item(i, "custom_support_list")
    
    def add_and_clear_support():
        if st.session_state.new_support_input.strip():  # Only add non-empty support
            add_item(st.session_state.new_support_input, st.session_state.custom_support_list)
            st.session_state.new_support_input = ""

    # Add new support source
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input(
            "Add support source here:",
            placeholder="Enter support source...",
            key="new_support_input",
            label_visibility="collapsed",
            help=""
        )
    with col2:
        st.button("Add", 
                 type="primary", 
                 key="add_support_button",
                 on_click=add_and_clear_support)
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    # Navigation buttons
    gif_path = get_gif_path(st.session_state.current_step)
    col_agent, col_back, col_next = st.columns([8, 1, 1])
    
    with col_back:
        st.button("Back", on_click=prev_step)
    
    with col_next:
        # Combine support strings only when clicking Next
        if st.button("Next", on_click=next_step):
            selected_support = st.session_state.form_data[step_name]
            custom_support = ", ".join(st.session_state.custom_support_list)
            
            if selected_support and custom_support:
                combined_support = f"{selected_support}, {custom_support}"
            else:
                combined_support = selected_support or custom_support
                
            st.session_state.form_data["support_system"] = combined_support
        
    with col_agent:
        display_agent_section(step_name, gif_path, "user has shared their support system now, it might be empty though, discuss the support system with the user")

def render_strengths_step():
    st.divider()
    st.markdown('<p class="section-title">✨ Positive Thinking: Your Strengths</p>', unsafe_allow_html=True)
    
    strengths = st.multiselect(
        "What personal strengths can help you in this situation?",
        [
            "Resilience",
            "Creativity",
            "Determination",
            "Empathy",
            "Problem-solving",
            "Communication",
            "Adaptability",
            "Patience",
            "Leadership",
            "Self-awareness",
            "Optimism",
            "Analytical thinking",
            "Emotional intelligence",
            "Organization",
            "Perseverance",
            "Active listening",
            "Growth mindset",
            "Self-motivation"
        ],
        help="Recognizing your strengths is important for growth"
    )
    
    # Custom strengths section
    st.markdown("##### ✨ Or add your own strengths:")
    
    # Display existing custom strengths with delete buttons
    for i, strength in enumerate(st.session_state.custom_strengths_list):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f'<div class="custom-thought-box">'
                      f'<span class="thought-text">{strength}</span>'
                      f'</div>', 
                      unsafe_allow_html=True)
        with col2:
            st.write("")  # Add spacing to align with text
            if st.button("🗑️", key=f"delete_strength_{i}", help="Delete this strength"):
                delete_item(i, "custom_strengths_list")
    
    def add_and_clear_strength():
        if st.session_state.new_strength_input.strip():  # Only add non-empty strength
            add_item(st.session_state.new_strength_input, st.session_state.custom_strengths_list)
            st.session_state.new_strength_input = ""

    # Add new strength
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input(
            "Add your strength here:",
            placeholder="Enter another strength...",
            key="new_strength_input",
            label_visibility="collapsed",
            help="",
            on_change=add_and_clear_strength
        )
    with col2:
        st.button("Add", 
                 type="primary", 
                 key="add_strength_button",
                 on_click=add_and_clear_strength)
    
    # Convert selected strengths to string and combine with custom strengths
    selected_strengths = ", ".join(strengths) if strengths else ""
    custom_strengths_str = ", ".join(st.session_state.get("custom_strengths_list", []))
    
    # Combine strings with comma if both exist
    if selected_strengths and custom_strengths_str:
        all_strengths = f"{selected_strengths}, {custom_strengths_str}"
    else:
        all_strengths = selected_strengths or custom_strengths_str
        
    st.session_state.form_data["strengths"] = all_strengths
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    step_name = "strengths"
    gif_path = get_gif_path(st.session_state.current_step)
    col_agent, col_back, col_next = st.columns([8, 1, 1])
    
    with col_back:
        st.button("Back", on_click=prev_step)
    
    with col_next:
        def handle_next():
            # Convert selected strengths (list) to string
            selected_strengths = ", ".join(strengths) if strengths else ""
            # Convert custom strengths to string
            custom_strengths = ", ".join(st.session_state.get("custom_strengths_list", []))
            
            # Combine strings with comma if both exist
            if selected_strengths and custom_strengths:
                combined_strengths = f"{selected_strengths}, {custom_strengths}"
            else:
                combined_strengths = selected_strengths or custom_strengths
                
            # Store the combined string
            st.session_state.form_data[step_name] = combined_strengths
            next_step()
            
        st.button("Next", on_click=handle_next)
        
    with col_agent:
        display_agent_section(step_name, gif_path, "user has shared their strengths now, discuss the strengths with the user")

def render_goals_step():
    st.divider()
    step_name = "goal"
    st.markdown('<p class="section-title">🎯 Positive Thinking: Looking Forward</p>', unsafe_allow_html=True)
    
    # Load existing goal from session state if it exists
    existing_goal = st.session_state.form_data.get("goal", "")
    
    goal = st.text_area(
        "What small steps would you like to take towards feeling better?",
        value=existing_goal,  # Load existing value
        placeholder="Example: I want to practice self-care for 10 minutes daily",
        help="Start with small, achievable goals"
    )
    
    st.session_state.form_data[step_name] = goal
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    gif_path = get_gif_path(st.session_state.current_step)
    col_agent, col_back, col_next = st.columns([8, 1, 1])
    
    with col_back:
        st.button("Back", on_click=prev_step)
    
    with col_next:
        st.button("Next", on_click=next_step)
        
    with col_agent:
         display_agent_section(step_name, gif_path, "user shared small steps to take towards feeling better, discuss the goal with the user")

def render_final_step():
    st.divider()
    st.markdown('<p class="section-title">💝 Final Thoughts</p>', unsafe_allow_html=True)
    
    # Load existing extra notes from session state
    existing_notes = st.session_state.form_data.get("extra_notes", "")
    
    extra = st.text_area(
        "Anything else you'd like to share?",
        value=existing_notes,  # Load existing value
        help="This is your space to express anything additional",
        placeholder="Optional: Share any other thoughts or feelings..."
    )
    
    # Use 'extra_notes' as the key to match where it's used
    step_name = "extra_notes"
    st.session_state.form_data[step_name] = extra
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    gif_path = get_gif_path(st.session_state.current_step)
    col_agent, col_back, col_next = st.columns([8, 1, 1])
    
    with col_back:
        st.button("Back", on_click=prev_step)
    
    with col_next:
        def handle_submit():
            st.session_state.form_data["submitted"] = True
            next_step()
            
        st.button("next", on_click=handle_submit)
        
    with col_agent:
        display_agent_section(step_name, gif_path, "user shared some extra notes now, discuss the extra notes with the user")

def render_summary_step():
    st.divider()
    st.markdown('<p class="section-title">💝 Summary</p>', unsafe_allow_html=True)
    
    # Display all collected information in styled boxes
    st.markdown("""
        <div class="summary-box">
            <h5>💭 Your Situation</h5>
            <p><strong>Area of Concern:</strong> {}</p>
            <p>{}</p>
        </div>
    """.format(
        st.session_state.form_data.get('category', ''),
        st.session_state.form_data.get('situation', '')
    ), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="summary-box">
            <h5>💗 Your Emotions</h5>
            <p><strong>Primary Emotion:</strong> {}</p>
            <p><strong>Intensity:</strong> {}</p>
        </div>
    """.format(
        st.session_state.form_data.get('primary_emotion', ''),
        st.session_state.form_data.get('emotion_intensity', '').strip()
    ), unsafe_allow_html=True)
    
    support = st.session_state.form_data.get("support_system", [])
    if support:
        # Check if support is a string and convert it to list if needed
        if isinstance(support, str):
            # Split the string by commas and strip whitespace
            support_list = [item.strip() for item in support.split(",") if item.strip()]
        else:
            support_list = support

        # Create HTML list items
        support_html = "\n".join([f"<li>{item}</li>" for item in support_list])
        st.markdown(f"""
            <div class="summary-box">
                <h5>👥 Your Support Network</h5>
                <ul>{support_html}</ul>
            </div>
        """, unsafe_allow_html=True)
    
    strengths = st.session_state.form_data.get("strengths", [])
    if strengths:
        # Check if strengths is a string and convert it to list
        if isinstance(strengths, str):
            # Split the string by commas and strip whitespace
            strengths_list = [item.strip() for item in strengths.split(",") if item.strip()]
        else:
            strengths_list = strengths

        # Create HTML list items
        strengths_html = "\n".join([f"<li>{strength}</li>" for strength in strengths_list])
        
        st.markdown(f"""
            <div class="summary-box">
                <h5>✨ Your Strengths</h5>
                <ul>{strengths_html}</ul>
            </div>
        """, unsafe_allow_html=True)
    if st.session_state.form_data.get('goal'):  # Only show if goal exists
        st.markdown("""
            <div class="summary-box">
                <h5>🎯 Looking Forward</h5>
                <p><strong>Your Next Step:</strong> {}</p>
            </div>
        """.format(
            st.session_state.form_data.get('goal', '')
        ), unsafe_allow_html=True)

    if st.session_state.form_data.get("extra_notes"):
        st.markdown(f"""
            <div class="summary-box">
                <h5>💌 Additional Thoughts</h5>
                <p>{st.session_state.form_data.get('extra_notes')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Add vertical spacing
    st.write("")
    st.write("")
    
    # Final submit button
    col1, spacer1, spacer2, col3 = st.columns([1, 2, 2, 3])
    with col1:
        if st.button("Back", key="summary_back", help="Return to previous step"):
            st.session_state.current_step = 7  # Go back to final step
            st.rerun()
    with col3:
        if st.button("✨ Get Personalized Support", 
                    type="primary",
                    on_click=next_step,
                    help="Transform your situation into personalized guidance"):
            print("Debug: Convert button clicked")
            
            # Set form data and submission flag
            st.session_state.form_data["submitted"] = True
            
            # Change page state to loading
            st.session_state.page = "loading"
            print("Debug: Switching to loading page")
            st.rerun()

def render_response_step():
    st.empty()
    placeholder = st.container()
    
    def get_base64_gif(gif_path):
        with open(gif_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
    
    with placeholder:
        st.markdown('<p class="section-title">💫 Your Personalized Support</p>', unsafe_allow_html=True)
        
        # Only generate AI response if it hasn't been generated yet
        if "ai_response" not in st.session_state:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                gif_path = "static/gif/bird.gif"
                gif_base64 = get_base64_gif(gif_path)
                st.markdown(f"""
                    <div style="display: flex; justify-content: center;">
                        <img src="data:image/gif;base64,{gif_base64}" width="150px">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown("""
                    ##### You've Taken an Important Step
                    
                    Thank you for sharing your journey with us. By reflecting on your experiences and seeking support, you've shown great courage and self-awareness. 
                    Remember, every step forward, no matter how small, is progress. You have the strength within you to create positive change.
                """)
        

            with st.spinner("Generating your personalized support message..."):
                st.session_state.ai_response = generate_ai_response(st.session_state.form_data)
        
        if "ai_response" in st.session_state:
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "🤗 Validation",
                "💡 Insights",
                "🎯 Milestones",
                "✨ Actions",
                "👥 Support",
                "🌱 Growth",
                "🎬 Helpful Youtube Videos"
            ])
            
            # Validation Tab
            with tab1:
                st.markdown("""
                    <div class="response-box validation">
                        <h4>Understanding Your Experience</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("validation", "")), unsafe_allow_html=True)
            
            # Insights Tab
            with tab2:
                st.markdown("""
                    <div class="response-box insights">
                        <h4>Key Insights & Reflections</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("insights", "")), unsafe_allow_html=True)
            
            # Milestones Tab
            with tab3:
                st.markdown("""
                    <div class="response-box milestones">
                        <h4>Your Strengths & Progress</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("milestones", "")), unsafe_allow_html=True)
            
            # Actions Tab
            with tab4:
                st.markdown("""
                    <div class="response-box actions">
                        <h4>Practical Next Steps</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("actions", "")), unsafe_allow_html=True)
            
            # Support Tab
            with tab5:
                st.markdown("""
                    <div class="response-box support">
                        <h4>Support Network & Resources</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("support", "")), unsafe_allow_html=True)
            
            # Growth Tab
            with tab6:
                st.markdown("""
                    <div class="response-box growth">
                        <h4>Growth & Development</h4>
                        <p>{}</p>
                    </div>
                """.format(st.session_state.ai_response.get("growth_overview", "")), unsafe_allow_html=True)

            # Videos Tab
            with tab7:
                if "youtube_videos" not in st.session_state:
                    # Generate search query based on the situation and category
                    search_query = f"deal with {st.session_state.form_data['category']} problems"
                    print(search_query)
                    
                    # Search for videos
                    videos = search_youtube_videos(
                        query=search_query,
                        api_key=st.secrets["GOOGLE_API_KEY"],
                        max_results=5
                    )
                    
                    st.session_state.youtube_videos = videos
                
                st.markdown("""
                    <div class="response-box videos">
                        <h4>Recommended Videos</h4>
                        <p>Here are some helpful videos related to your situation:</p>
                    </div>
                """, unsafe_allow_html=True)

                # Display videos
                for video in st.session_state.youtube_videos:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(video['thumbnail'], use_container_width=True)
                    with col2:
                        st.markdown(f"#### {video['title']}")
                        st.markdown(video['description'][:200] + "..." if len(video['description']) > 200 else video['description'])
                        st.markdown("""
                                    <div>
                                        <a href="https://www.youtube.com/watch?v={video['video_id']}" target="_blank" class="yellow-link">Watch Video</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    st.divider()                
def generate_ai_response(form_data):
    try:
        print("Generating AI response")
        # Configure and use the LLM
        llm_api_key = st.session_state.get('gemini_api_key')
        genai.configure(api_key=llm_api_key)
        model = genai.GenerativeModel(model_name="gemini-pro")
        
        # Get previous responses if they exist
        previous_responses = ""
        if "step_responses" in st.session_state:
            previous_responses = "\nPrevious step interactions:\n"
            for step, response in st.session_state.step_responses.items():
                previous_responses += f"Step '{step}': {response}\n"

        # Build prompt with previous responses
        prompt = build_empowerment_prompt(
            category=form_data["category"],
            situation=form_data["situation"],
            thoughts=form_data["thoughts"],
            emotions=form_data["primary_emotion"],
            emotion_intensity=form_data["emotion_intensity"],
            support_system=form_data["support_system"],
            strengths=form_data["strengths"],
            goal=form_data["goal"],
            extra_notes=form_data["extra_notes"],
            previous_responses=previous_responses  # Add previous responses
        )
        
        # Generate response
        response = model.generate_content(prompt)
        
        raw_text = response.candidates[0].content.parts[0].text
        
        sections = {
            "validation": "",
            "insights": "",
            "milestones": "",
            "actions": "",
            "support": "",
            "growth_overview": ""
        }
        
        # 定义section标记对
        section_markers = {
            "validation": ("[VALIDATION_START]", "[VALIDATION_END]"),
            "insights": ("[INSIGHTS_START]", "[INSIGHTS_END]"),
            "milestones": ("[MILESTONES_START]", "[MILESTONES_END]"),
            "actions": ("[ACTIONS_START]", "[ACTIONS_END]"),
            "support": ("[SUPPORT_START]", "[SUPPORT_END]"),
            "growth_overview": ("[GROWTH_START]", "[GROWTH_END]")
        }
        
        def extract_section(text, start_marker, end_marker):
            try:
                start_idx = text.find(start_marker)
                if start_idx == -1:
                    return ""
                
                # 从开始标记后开始查找结束标记
                content_start = start_idx + len(start_marker)
                end_idx = text.find(end_marker, content_start)
                
                if end_idx == -1:
                    return ""
                
                # 提取内容并清理
                content = text[content_start:end_idx].strip()
                # 将星号标记转换为圆点
                content = content.replace("* ", "• ")
                # 移除空行
                content = "\n".join(line.strip() for line in content.split("\n") if line.strip())
                
                return content
            except Exception as e:
                print(f"Error extracting section: {e}")
                return ""
        
        for section, (start_marker, end_marker) in section_markers.items():
            sections[section] = extract_section(raw_text, start_marker, end_marker)
        
        return sections
        
    except Exception as error:
        st.error(f"Error generating response: {str(error)}")
        print(f"Error details: {error}")
        return None
    
def search_youtube_videos(query, api_key, max_results=5):
    """
    Search for YouTube videos related to the situation
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Call the search.list method to retrieve results matching the specified query term
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            relevanceLanguage='en',
            safeSearch='strict'
        ).execute()
        
        videos = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append({
                    'title': search_result['snippet']['title'],
                    'description': search_result['snippet']['description'],
                    'video_id': search_result['id']['videoId'],
                    'thumbnail': search_result['snippet']['thumbnails']['medium']['url']
                })
        
        return videos
    
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []
    
def generate_robot_response(form_data, extra_prompt: str = ""):
    try:
        # Configure the Gemini API
        llm_api_key = st.session_state.get('gemini_api_key')
        genai.configure(api_key=llm_api_key)
        model = genai.GenerativeModel(model_name="gemini-pro")


        # Extract values, defaulting to empty strings if not present
        situation = form_data.get("situation", "")
        category = form_data.get("category", "")
        thoughts = form_data.get("thoughts", "")
        emotions = form_data.get("emotions", "sad")
        emotion_intensity = form_data.get("emotion_intensity", "mild")
        support_system = form_data.get("support_system")
        strengths = form_data.get("strengths", "")
        goal = form_data.get("goal", "")
        extra_notes = form_data.get("extra_notes", "")


        # Get previous responses if they exist
        previous_responses = ""
        if "step_responses" in st.session_state:
            previous_responses = "\nPrevious interactions with the user:\n"
            for step, response in st.session_state.step_responses.items():
                previous_responses += f"Step '{step}': {response}\n"

        # Construct the prompt dynamically
        prompt = (
            f'''The user described their situation as:
            Context:
                - Category: {category}
                - Situation: {situation}
                - Current Thoughts: {thoughts}
                - Emotional State: {emotions}
                - Emotion Intensity: {emotion_intensity.strip()}
                - Available Support: {support_system}
                - Personal Strengths: {strengths}
                - Goal: {goal}
                - Additional Notes: {extra_notes}

            Previous Agent Interactions:
            {previous_responses}
            {crisis_support_resources}

            Extra Prompt:
            {extra_prompt if extra_prompt else ""}

            As an AI agent for HerSpace, please respond with encouraging and supportive messages. 
            Remember, users may feel vulnerable while filling out this form, so it's important to be empathetic and understanding.
            Ignore the empty context.
            Don't mention the type of the response, just respond as a friend would.

            If at any point a user feels uneasy about sharing their thoughts or experiences, reassure them that it’s perfectly okay to take a break or stop the process. 
            Encourage them to explore "Crisis Support Resources" and "Therapy Location Finder" on the sidebar on this site (we only have these two pages for now) if they need to step away for a moment.
            If the situation is about violence, abuse, crisis, crime, or other serious issues, encourage them to to explore "Crisis Support Resources" and "Therapy Location Finder" page and seek professional help.
            Your role is to create a safe and supportive environment for their journey.

            You're a HerSpace Agent, so don't include string like "[your name], Crisis Support: [link], Therapy Location Finder: [link]" in your response because you're not writing a template for others.
            '''
        )
        print(prompt)

        # Generate the response
        response = model.generate_content(prompt)

        # Check if the response contains candidates
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.finish_reason == "SAFETY":
                return "I'm here to support you! It's great that you've recognized this issue. Acknowledging your feelings is a significant step towards growth, and I'm here to help you through this journey."
            else:
                return candidate.content.parts[0].text.strip()
        else:
            return "I'm here to support you! It's great that you've recognized this issue. Acknowledging your feelings is a significant step towards growth, and I'm here to help you through this journey."

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm here to support you! Remember, every step you take is a step towards growth."

def display_ai_response(step_name: str, gif_path: str, extra_prompt: str = "") -> str:
    """
    Display AI response with GIF and store the response in session state.
    
    Args:
        step_name: The name of the current step (e.g., 'emotions', 'thoughts', etc.)
        
    Returns:
        str: The generated response
    """
    with st.spinner("Generating response... Please wait."):
        # Generate and display the robot's response
        robot_response = generate_robot_response(st.session_state.form_data, extra_prompt)
        
        # Store the response in session state with step name
        if 'step_responses' not in st.session_state:
            st.session_state.step_responses = {}
        st.session_state.step_responses[step_name] = robot_response

        # Display the GIF and the response
        col1InResponse, col2InResponse = st.columns([1, 2])
        
        with col1InResponse:
            st.image(gif_path, use_container_width=True)

        with col2InResponse:
            st.markdown(
                f"""<div class='ai-response-container'>
                    <p class='ai-response-text'>{robot_response}</p>
                </div>""", 
                unsafe_allow_html=True
            )
        
        return robot_response
    

def get_gif_path(step_name: str) -> str:
    return f"./static/gif/{step_name}.gif"

def display_agent_section(step_name: str, gif_path: str, extra_prompt: str = ""):
    """
    Display the AI agent section with support button and previous/new responses.
    
    Args:
        step_name: Current step name (e.g., 'situation', 'thoughts')
        gif_path: Path to the GIF file to display
        col1: Streamlit column object where the section should be displayed
    """
    if st.button("🤖 Need supportive response from HerSpace Agent now?", 
                help="If you feel uneasy after describing your situation, you can click the button below to receive support from a HerSpace agent. If you don't need support right now, feel free to click 'Next' to proceed."):
        display_ai_response(step_name, gif_path, extra_prompt)
    else:
        # Check and display previous response if exists
        if "step_responses" in st.session_state and step_name in st.session_state.step_responses:
            col1InResponse, col2InResponse = st.columns([1, 5])
            with col1InResponse:
                st.image(gif_path, use_container_width=True)
            with col2InResponse:
                st.markdown(
                    f"""<div class='ai-response-container'>
                        <p class='ai-response-text'>last response: {st.session_state.step_responses[step_name]}</p>
                    </div>""", 
                    unsafe_allow_html=True
                )