"""test_app.py"""

from streamlit.testing.v1 import AppTest
at = AppTest.from_file("main_menu.py").run()
