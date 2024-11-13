import time
import streamlit as st
from home.steps import (render_welcome_step, render_thoughts_step, 
                  render_emotions_step, render_support_step,
                  render_strengths_step, render_goals_step,
                  render_final_step, render_summary_step,
                  render_response_step, init_session_state)


def get_empowerment_solution():
    # Initialize session states
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    if "custom_thoughts" not in st.session_state:
        st.session_state.custom_thoughts = []
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}

    # Navigation functions
    def next_step():
        st.session_state.current_step += 1

    def prev_step():
        st.session_state.current_step -= 1

    def add_thought(new_thought, thoughts):
        if new_thought and new_thought not in st.session_state.custom_thoughts:
            st.session_state.custom_thoughts.append(new_thought)
            st.session_state.form_data["thoughts"] = thoughts + [new_thought]

    def delete_thought(index):
        st.session_state.custom_thoughts_list.pop(index)
        st.rerun()
    # Initialize session state
    init_session_state()
    
    # Render appropriate step
    # Step 1: Welcome
    if st.session_state.current_step == 1:
        render_welcome_step()

    # Step 2: Thoughts
    elif st.session_state.current_step == 2:
        render_thoughts_step()

    # Step 3: Emotions
    elif st.session_state.current_step == 3:
        render_emotions_step()

    # Step 4: Support System
    elif st.session_state.current_step == 4:
        render_support_step()

    # Step 5: Strengths Recognition
    elif st.session_state.current_step == 5:
        render_strengths_step()

    # Step 6: Goals
    elif st.session_state.current_step == 6:
        render_goals_step()
        
    # Step 7: Final Thoughts
    elif st.session_state.current_step == 7:
        render_final_step()

    elif st.session_state.current_step == 8:
        render_summary_step()
            
    elif st.session_state.current_step == 9:
        render_response_step()
        print("Form submitted ")
        # Add some spacing
        st.write("")
        st.write("")
        
        # Add Start Over button centered
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("✨ Start Over", type="primary"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                # Reinitialize current_step to 1
                st.session_state.current_step = 1
                print("st.session_state.current_step ", st.session_state.current_step)
                st.rerun()

        return st.session_state.form_data
    
    return None
