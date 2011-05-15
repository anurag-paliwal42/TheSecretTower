#-*-coding:Utf-8 -*
# Auteur : Pierre Surply

import element

class Text(Element):
    """ Texte """

    def __init__(self, text, font):
        self.element.changer_text(text)
        
        
