import streamlit as st
st.divider()
crisis_support_resources = """
    <div class="response-box crisis-support">
            <p class="subtitle">In an emergency, remember that you're not alone. Here are resources available for urgent, expert support.</p>
            <ul>
            <li><strong>Suicide Prevention</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>Suicide and Crisis Lifeline: <strong>988</strong></li>
                    <li>Crisis Text Line: Text <strong>TRUST</strong> at 741741</li>
                    <li>Veterans Crisis Line: For veterans - <strong> 1-800-273-8255</strong></li>
                    <li>
                        National Alliance for Eating Disorders: 
                        <strong>1-866-662-1235</strong> 
                        <a href="https://www.allianceforeatingdisorders.com/" target="_blank" class="yellow-link">Website Link</a>
                    </li>                                
                </ul>
            </li>
            <li><strong>Domestic Violence</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>Love is Respect - National Teen Dating Abuse Hotline: <strong>1-866-331-9474</strong> 
                        <a href="https://www.loveisrespect.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>National Domestic Violence Hotline: <strong>1-800-799-SAFE (7233)</strong> 
                        <a href="https://www.thehotline.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>StrongHearts Native Helpline: <strong>1−844-762-8483</strong> 
                        <a href="https://strongheartshelpline.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>Office on Violence Against Women: <strong>1-202-307-6026</strong> 
                        <a href="https://www.justice.gov/ovw" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                </ul>
            </li>
            <li><strong>Sexual Assault and Harassment</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>National Sexual Assault Hotline: <strong>1-800-656-HOPE(4673)</strong> 
                        <a href="https://hotline.rainn.org/online" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>National Street Harassment Hotline: <strong>1-855-897-5910</strong> 
                        <a href="https://hotline.rainn.org/ssh-en" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                </ul>
            </li>
            <li><strong>Non-consensual Intimate Images</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>Cyber Civil Rights Initiative: <strong>1-844-878-2274</strong> 
                        <a href="https://cybercivilrights.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>Love Is Respect: <strong>1-866-331-9474</strong> 
                        <a href="https://www.loveisrespect.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>Take It Down: 
                        <a href="https://takeitdown.ncmec.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>Thorn: 
                        <a href="https://www.thorn.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                </ul>
            </li>
            <li><strong>LGBTQ+ Helplines</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>The Trevor Project: Helpline: <strong>1-866-488-7386</strong> or Text “Start” to 678678 
                        <a href="https://www.thetrevorproject.org/get-help/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                </ul>
            </li>
            <li><strong>Child Protection</strong>
                <br><br>
                <ul class="faq-answer">
                    <li>Childhelp: 
                        <a href="https://www.childhelphotline.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>National Center for Missing and Exploited Children: 
                        <a href="https://www.missingkids.org/home" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                    <li>Thorn: 
                        <a href="https://www.thorn.org/" target="_blank" class="yellow-link">Website Link</a>
                    </li>
                </ul>
            </li>
        </ul>
        <p><em>🌍 Note: We are actively collecting crisis support resources for more countries. If you know of critical support services in your region, please help us expand this list.</em></p>

    </div>
"""
st.markdown(crisis_support_resources, unsafe_allow_html=True)