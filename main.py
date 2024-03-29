from lark import Lark
from textwrap import dedent
from random import randint

grammar = ''' 
    start: (cast | action | inventory_action | open_inventory | book | help) [PUNCTUATION]
            | exit [PUNCTUATION]

    cast: "cast" SPELL [PREPOSITION] ["the" | "a"] OBJECT 

    action: VERB [PREPOSITION] ["the" | "a"] OBJECT 

    inventory_action: use | add  | drop | drink

    open_inventory: "open inventory" | "open backpack"

    exit: "end game" | "exit game" | "escape" | "exit"

    use: "use" ["the"] ITEM [PREPOSITION] ["the"] [OBJECT] 

    add: ("pickup" | "add") ["the"] ITEM 

    drop: ("drop" | "remove" | "get rid of") ["the"] ITEM

    drink: ("drink" | "use") ["the"] "potion" 

    book: "read spellbook" | "open spellbook"

    help: "help" | "help me" 

    PUNCTUATION: "." | "!" | "?" | ","

    SPELL:  "fire" | "water" | "earth" | "air"
         
    VERB: "knock" | "break" | "enter" | "go inside" 

    PREPOSITION: "on" | "at" | "in"
                        
    OBJECT: "sprout" | "door" | "fireplace" | "mist" | "vines" | "embers" | "bookshelf" | "bookshelves" 
            | "knick-knack" | "book" | "volume" | "hole" | "void" | "sofa" | "paper"

    ITEM: "key" | "lantern" | "potion" | "dagger" | "spellbook" | "papers" | "hat" | "scarf" 

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
    elif tree.data == 'drink':
        return drink_potion()
    elif tree.data == 'open_inventory':
        return open_inventory()
    elif tree.data == 'book':
        return print_spells()
    elif tree.data == 'help':
        print_help()
    elif tree.data == 'exit':
        return end_game()
    else:
        return


### GAME FUNCTIONS ###

def cast_spell(spell, object):
    if spell == 'fire':
        if object == 'door':
            open_door()
        elif object == 'fireplace' or object == 'embers':
            print('\nThe fireplace erupts with a warm glow illuminating the room.\n')
        elif object == "vines":
            clear_vines()
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
        elif object == 'mist' or object == 'vines':
            random_reply()
        else:
            print('\nFor a moment ' + object + ' appears weathered and cracked and an')
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
    elif object == 'hole' or object == 'void' and verb == 'enter' or "go inside":
            enter_void()
    else:
        random_reply()


def use_item(item, object):
    if item == 'key' and object == 'door':
            open_door()
    elif item == 'dagger' and object == 'vines':
        clear_vines()
    elif item == "potion":
        drink_potion()
    else:
        random_reply()
    

def add_item(item):
    global inventory
    if item not in inventory:
        inventory.append(item)
        print('\n' + item + " added to your backpack\n")
    else:
        print('\n' + item + " is already in your backpack\n")


def drop_item(item):
    if item == 'spellbook':
        print('\nThe book almost hits the ground before it vanishes into thin air...')
        print('and reappears in your backpack.\n')
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


def print_help():
    print(dedent('''
    Help:
    Interact: <verb> the <object>
    Cast Spell: <cast> <spell> at <object>
    Open Inventory: <open> <backpack/inventory>
    Check Spells: <read spellbook>
    Use Item: <use> <item>
    End Game: <escape/exit>
    '''))


def clear_mist():
    print('\nThe mist crawls towards the treeline, revealing a single sprout in the center of the clearing.\n')


def reveal_door():
    print(dedent('''
    The sprout shoots farther and farther out of the earth. 
    It grows limbs that twist in on itself and become gnarled. 
    In place of the sprout a weathered old tree now stands. 
    
    At the base of the tree is a wooden door with a small stained glass window. A dim light glows behind it.  
    '''))


def open_door():
    print(dedent('''
    The door swings open to a round room. 
    It appears void of life other than the green vines obscuring much of the walls and floor.
    A fireplace sits on the far side, casting a slight glow from dying embers.
    There are bookshelves stuffed with old volumes and knick-knacks.

    A worn sofa sits in front of the fireplace next to a table with crumpled papers and a single potion.
    On the wall hangs a single hat and scarf along with a sheath containing a jeweled dagger.
    '''))


def drink_potion():
    print(dedent('''
    The room starts to spin slightly and the walls, the walls look like they are melting. 
    You lie down and close your eyes, willing it to stop.
    It does. When you open them you feel calm, almost peaceful.

    Everything looks normal.
    '''))


def clear_vines():
    print(dedent('''
    With the vines out of the way, you see a gaping hole in the floor.
    It's dark beyond, you cannot see anything.
    '''))


def enter_void():
    for i in range(0,10):
        print('\n')
    print(dedent('''
    After a long walk down a dank corridor, you see a glowing light. 
    As you get closer, a room comes into view.
    Inside someone eerily familiar sits in front of computer, staring at the screen. 
    '''))
    end_game()



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


if __name__ == '__main__':
    main()
