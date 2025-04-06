import UIHelpTools

refresh = UIHelpTools.refresh_screen
screen = UIHelpTools.original_content.copy()
insert_text = UIHelpTools.insert_text

def initial_UI():
    refresh(screen)

initial_UI()