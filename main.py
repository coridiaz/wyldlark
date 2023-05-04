from lark import Lark
from textwrap import dedent
from random import randint

grammar = ''' 
    start: ((cast | action | inventory_action | open_inventory | book) [PUNCTUATION])* | exit [PUNCTUATION]

    cast: "cast" SPELL [PREPOSITION] ["the" | "a"] OBJECT 

    action: VERB [PREPOSITION] ["the" | "a"] OBJECT 

    inventory_action: use | add  | drop

    open_inventory: "open inventory" | "open backpack"

    exit: "end game" | "exit game" | "escape" | "exit"

    use: "use" ["the"] ITEM [PREPOSITION OBJECT]

    add: ("pickup" | "add") ["the"] ITEM 

    drop: ("drop" | "remove" | "get rid of") ["the"] ITEM

    book: "read spellbook" | "open spellbook"

    PUNCTUATION: "." | "!" | "?" | ","

    SPELL:  "fire" | "water" | "earth" | "air"
         
    VERB: "knock" | "break"

    PREPOSITION: "on" | "at" | "in"
                        
    OBJECT: "sprout" | "door" | "fireplace" | "mist"

    ITEM: "key" | "lantern" | "potion" | "dagger" | "spellbook"

    %import common.WS 
    %ignore WS 
    '''


### GAME GLOBALS ###

global game
global inventory

game = True
inventory = ['spellbook', 'key']


### GRAMMAR FUNCTIONS ###

def translate(tree):
    if tree.data == 'start':
        for child in tree.children:
            return translate(child)
    elif tree.data == 'cast':
        return cast_spell(tree.children[0], tree.children[-1])
    elif tree.data == 'action':
        return perform_action(tree.children[0], tree.children[-1])
    elif tree.data == 'inventory_action':
        for child in tree.children:
            return translate(child)
    elif tree.data == 'use':
        return use_item(tree.children[0], tree.children[-1])
    elif tree.data == 'add':
        return add_item(tree.children[-1].value)
    elif tree.data == 'drop':
        return drop_item(tree.children[-1].value)
    elif tree.data == 'open_inventory':
        return open_inventory()
    elif tree.data == 'book':
        return print_spells()
    elif tree.data == 'exit':
        return end_game()
    else:
        return


def cast_spell(spell, object):
    if spell == 'fire':
        if object == 'door':
            open_door()
        elif object == 'fireplace':
            print('\nThe fireplace erupts with a warm glow illuminating the room.\n')
        elif object == 'mist':
            random_reply()
        else:
            print('\nThe ' + object + ' catches fire but a mysterious force smothers the flame.')
            print('The ' + object + ' remains unharmed.\n')
    elif spell == 'water':
        if object == 'sprout':
            reveal_door()
        elif object == 'mist':
            random_reply()
        else:
            print('\nThe ' + object + ' is doused with water but a mysterious force shields the ' 
                  + object + ' and it remains undisturbed.\n')
    elif spell == 'earth':
        if object == 'sprout':
            reveal_door()
        elif object == 'mist':
            random_reply()
        else:
            print('\nFor a moment it appears the ' + object + ' is weathered and cracked, and an')
            print('ancient presence fills the room. In a blink the feeling is gone.') 
            print('The ' + object + ' appears unphased.\n')
    elif spell == 'air':
        if object == 'mist':
            clear_mist()
        else:
            print("\nThe " + object + " receives a gust of wind but mysteriously remains undisturbed.\n")


def perform_action(verb, object):
    if object == 'door':
        if verb == 'knock':
            random_reply()
        elif verb == 'break':
            open_door()
    else:
        random_reply()


def use_item(item, object):
    if item == 'key':
        if object == 'door':
            open_door()
        else:
            random_reply()
    else:
        random_reply()
    

### GAME FUNCTIONS ###

def add_item(item):
    global inventory
    if item not in inventory:
        inventory.append(item)
        print('\n' + item + " added to your backpack\n")
    else:
        print('\n' + item + " is already in your backpack\n")


def drop_item(item):
    if item == 'spellbook':
        print('\nThe book almost hits the ground before it vanishes into thin air...\nand reappears in your backpack.\n')
    else:
        global inventory
        if item in inventory:
            inventory.remove(item)
            print('\n' + item + " has been removed from your backpack\n")
        else:
            print('\nYou do not have a ' + item + " in your backpack\n")


def open_inventory():
    global inventory
    print("\nBackpack Inventory:")
    for item in inventory:
        print(item)
    print('\n')


def print_spells():
    print(dedent('''
    Spells: 
    fire - creates flame
    water - creates stream of water
    earth - grows living things
    air - creates gust of wind
    '''))


def clear_mist():
    print('\nThe mist crawls towards the treeline, revealing a single sprout in the center of the clearing.\n')


def reveal_door():
    print(dedent('''
    The sprout shoots farther and farther out of the earth. It grows limbs that twist in on itself and become gnarled. 
    In place of the sprout a weathered old tree now stands. 
    
    At the base of the tree is a wooden door with a small stained glass window. A dim light glows behind it.  
    '''))


def open_door():
    print(dedent('''
    The door swings open to a round room...
    '''))
    

def random_reply():
    responses = ('*crickets*', 'nothing happens.', '*gentle breeze*', '*trees groaning*')
    print("\n" + responses[randint(0,3)] + "\n")  


def end_game():
    print("\nGoodbye.")
    global game
    game = False


def main():
    parser = Lark(grammar)

    print(dedent('''
    Welcome to Wyldlark\n
    You find yourself in the middle of a vast forest clearing.
    All around are towering Oak Trees and mist.\n
    You carry a backpack containing a battered leather spellbook and an iron key 
    with an ornate leaf on its handle.
    '''))

    while game == True:
        user_input = input('>> ')
        try:
            parse_tree = parser.parse(user_input)
            translate(parse_tree)
        except:
            random_reply()


    ### TESTING ### 

    # user_input = 'cast earth at fireplace'
    # user_input = 'read spellbook'
    # user_input = "pickup dagger"

    # try:
    #     parse_tree = parser.parse(user_input)
    #     translate(parse_tree)
    # except:
    #     random_reply()  

    # print(parse_tree.pretty())

if __name__ == '__main__':
    main()
