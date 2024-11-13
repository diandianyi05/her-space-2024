from contextlib import contextmanager

from deprecation import deprecated
import streamlit as st
import streamlit.components.v1 as components


class Modal:

    def __init__(self, title, key, padding=20, max_width=None):
        self.title = title
        self.padding = padding
        self.max_width = max_width
        self.key = key

    def is_open(self):
        return st.session_state.get(f'{self.key}-opened', False)

    def open(self):
        st.session_state[f'{self.key}-opened'] = True
        st.rerun()

    def close(self, rerun_condition=True):
        st.session_state[f'{self.key}-opened'] = False
        if rerun_condition:
            st.rerun()

    @contextmanager
    def container(self):
        if self.max_width:
            max_width = str(self.max_width) + "px"
        else:
            max_width = 'unset'

        st.markdown(
            f"""
            <style>
            div[data-modal-container='true'][key='{self.key}'] {{
                position: fixed;
                width: 100vw !important;
                left: 0;
                z-index: 1001;
                font-size: 1.5rem;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                margin: auto;
                top: 50px;
            }}

            div[data-modal-container='true'][key='{self.key}'] h1 a {{
                display: none
            }}

            div[data-modal-container='true'][key='{self.key}']::before {{
                    position: fixed;
                    content: ' ';
                    left: 0;
                    right: 0;
                    top: 0;
                    bottom: 0;
                    z-index: 1000;
                    background-color: rgba(0, 0, 0, 0.5);
            }}
            div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                max-width: {max_width};
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child {{
                width: unset !important;
                background-color: #fff;
                padding: {self.padding}px;
                margin-top: {2*self.padding}px;
                margin-left: -{self.padding}px;
                margin-right: -{self.padding}px;
                margin-bottom: -{2*self.padding}px;
                z-index: 1001;
                border-radius: 15px 15px 15px 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                max-height: 70vh;
                overflow-y: auto;
                overflow-x: hidden;
                direction: rtl;
                text-align: left;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child > * {{
                direction: ltr;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child::-webkit-scrollbar {{
                width: 20px;
                height: 10px;
                background-color: #FFE4E1;
                border-radius: 30px;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child::-webkit-scrollbar-track {{
                background: #f1f1f1;
                border-radius: 30px;
                height: 30px;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child::-webkit-scrollbar-thumb {{
                background: #FFC0CB;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child::-webkit-scrollbar-thumb:hover {{
                background: #555;
            }}

            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2)  {{
                z-index: 1003;
                position: absolute;
            }}
            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div {{
                text-align: right;
                padding-right: {self.padding}px;
                max-width: {max_width};
            }}

            div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div > button {{
                right: 0;
                margin-top: {2*self.padding + 14}px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.container():
            _container = st.container()
            if self.title:
                _container.markdown(
                    f"<h2>{self.title}</h2>", unsafe_allow_html=True)

        components.html(
            f"""
            <script>
            // STREAMLIT-MODAL-IFRAME-{self.key} <- Don't remove this comment. It's used to find our iframe
            const iframes = parent.document.body.getElementsByTagName('iframe');
            let container
            for(const iframe of iframes)
            {{
            if (iframe.srcdoc.indexOf("STREAMLIT-MODAL-IFRAME-{self.key}") !== -1) {{
                container = iframe.parentNode.previousSibling;
                container.setAttribute('data-modal-container', 'true');
                container.setAttribute('key', '{self.key}');
            }}
            }}
            </script>
            """,
            height=0, width=0
        )

        with _container:
            yield _container
