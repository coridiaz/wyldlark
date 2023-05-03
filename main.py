from lark import Lark, Transformer
from textwrap import dedent
from random import randint

grammar = ''' 
    start: ((cast | action | inventory_action) [punctuation])* | exit [punctuation]

    cast: "cast" spell [preposition] ["the" | "a"] object 

    action: verb [preposition] ["the" | "a"] object 

    inventory_action: use | add | "read spellbook" | "open backpack"

    exit: "end game" | "exit game" | "escape"

    use: "use" item [preposition object]

    add: "pickup" item

    punctuation: "." | "!" | "?" | ","

    spell:  "fire" | "water" | "earth" | "air"
         
    verb: "knock" | "break"

    preposition: "on" | "at" | "in"
                        
    object: "sprout"
            | "door"
            | "fireplace"
            | "mist"

    item: "spellbook"
        | "key"
        | "lantern"
        | "potion"
        | "dagger"

    %import common.WS 
    %ignore WS 
    '''


class GrammarTransformer(Transformer):
    def get_spell(self, item):
        # print('here\n')
        print(item)
        # return item[0]
    
    def get_object(self, item):
        return item[-1]


### GAME GLOBALS ###

global game
global inventory

game = True
inventory = ["spellbook"]


### GRAMMAR FUNCTIONS ###

def translate(tree):
    transformer = GrammarTransformer()
    # print(tree)
    if tree.data == 'start':
        for child in tree.children:
            return translate(child)
    elif tree.data == 'cast':
        for child in tree.children:
            return translate(child)
    elif tree.data == 'spell':
        return cast_spell(tree, transformer)
    elif tree.data == 'action':
        pass
    elif tree.data == 'inventory_action':
        # for child in tree.children:
        #     return translate(child)
        pass
    elif tree.data == 'exit':
        return end_game()
    else:
        return


def cast_spell(tree, transformer):
    # print(transformer.get_spell(tree) + '\n')
    transformer.get_spell(tree)
    # print(tree)


#     if tree.data == 'spell':
#         for child in tree.children:
#             return translate_spell(child)
#     elif tree.data == 'fire':
#         for child in tree.children:
#             return translate_spell(child)
#     elif tree.data == 'water':
#         pass
#     elif tree.data == 'earth':
#         pass
#     elif tree.data == 'air':
#         pass




### GAME FUNCTIONS ###

def add_object(object):
    global inventory
    if object not in inventory:
        inventory.append(object)
        return inventory
    else:
        print(object + " is already in your backpack")


def use_object(object):
    pass


def end_game():
    print("\nGoodbye.")
    global game
    game = False


def main():
    parser = Lark(grammar)
    responses = ('*crickets*', 'nothing happens.', '*gentle breeze*')

    print(dedent('''
    Welcome to _____\n
    You find yourself in the middle of a vast forest clearing.
    All around are towering Oak Trees and mist.\n
    You carry a backpack containing a battered leather spellbook.
    '''))

    # while game == True:
    #     user_input = input('>> ')
    #     try:
    #         parse_tree = parser.parse(user_input)
    #         translate(parse_tree)
    #     except:
    #         print("\n" + responses[randint(0,2)] + "\n")


    ### TESTING ### 

    user_input = 'cast air at mist'
    try:
        parse_tree = parser.parse(user_input)
        translate(parse_tree)
    except:
        print("\n" + responses[randint(0,2)] + "\n")    


if __name__ == '__main__':
    main()



# cast fire at object -> object burns and then magically...