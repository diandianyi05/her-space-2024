import streamlit as st


# Question 1
st.markdown('<div class="subtitle">How can I send my questions or suggestions?</div>', unsafe_allow_html=True)
st.write("")
st.markdown('<div class="faq-answer">We love hearing from you! If you have any questions or suggestions to help us improve, please don’t hesitate to reach out at '
            '<a class="yellow-link" href="mailto:hb.yi2024@gmail.com">this email account</a>. Your feedback means the world to us, and we’re here to make your experience better.</div>', unsafe_allow_html=True)

# Question 2
st.markdown('<div class="subtitle">What are your privacy policies?</div>', unsafe_allow_html=True)
st.write("")
st.markdown('<div class="faq-answer">Your privacy is super important to us! Rest assured, this website doesn’t use cookies or store any of your personal information or chat logs. '
            'All the information you share goes directly to Google Gemini for processing, and we keep everything confidential.</div>', unsafe_allow_html=True)

# Question 3
st.markdown('<div class="subtitle">Should I provide personal information?</div>', unsafe_allow_html=True)
st.write("")
st.markdown(f'''
    <div class="faq-answer">
        We totally understand the need for privacy. We encourage you to obscure any personal details when sending us your questions or suggestions. 
        Please avoid sharing sensitive information to keep your experience safe and comfortable.<br> 
        If you feel unsafe or someone might be monitoring your online activity, here's
        <a href="https://support.google.com/chrome/answer/95589?hl=en&co=GENIE.Platform%3DDesktop" class="yellow-link">
            how to clear Chrome browsing history.
        </a>
    </div>
''', unsafe_allow_html=True)


# Question 4
st.markdown('<div class="subtitle">Can I quit filling out the questions on the home page if I feel uneasy?</div>', unsafe_allow_html=True)
st.write("")
st.markdown('<div class="faq-answer">Absolutely! Your comfort is our top priority. If at any point you feel uneasy or stressed while recalling memories, you can stop filling out the questions whenever you like. '
            'Take care of yourself first. We also encourage you to explore our "Crisis Support Resources" and "Therapy Location Finder" sections on the website. There are plenty of resources available to support you.</div>', unsafe_allow_html=True)

# Copyright Issues FAQ
st.markdown('<div class="subtitle">What are the copyright considerations for the content on this website?</div>', unsafe_allow_html=True)
st.write("")
st.markdown('<div class="faq-answer">We take copyright seriously and want to be transparent about the sources of our content. '
            'The static images used on this website were generated by Google ImageFx, and the music tracks were created using Google MusicFx. '
            'As we are currently on the waitlist for Google VideoFx, we have sourced GIFs from reputable sites such as '
            '<a href="https://giphy.com/" class="yellow-link" target="_blank">Giphy</a> and '
            '<a href="https://pixabay.com/gifs/" class="yellow-link" target="_blank">Pixabay</a>. <br><br>'
            'If you are a content creator and believe that your rights regarding any images or materials have been infringed upon, please don’t hesitate to reach out to us at '
            '<a class="yellow-link" href="mailto:hb.yi2024@gmail.com">this email account</a>. <br><br>'
            'We take these matters seriously and will ensure that any related content in question is removed within 24 hours. '
            'Please note that this website is not intended for commercial use, and we are committed to respecting the rights of all creators.</div>', unsafe_allow_html=True)