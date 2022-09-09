# -*- coding: utf-8 -*-


try:
    import  threading
    import time
    from pytimedinput import timedInput
except:
    print("Failed to load module. try pip3 install pytimedinput")
    

Hero_hp = 40
Orc_hp = 7
Dragon_hp = 20

Hero_damage = 2
Orc_damage = 1
Dragon_damage = 3

stop = False


mutex = threading.Lock()


def set_health(Hero, Orc, Dragon):
    global Hero_hp,Orc_hp,Dragon_hp
    Hero_hp = Hero
    Orc_hp = Orc
    Dragon_hp = Dragon


def Orc_process():
    global stop

    while True:
        time.sleep(1.5)
        if stop:
            break
        if Hero_hp <= 0:
            break
        attack(2)


def Dradon_process():
    global stop

    while True:
        time.sleep(2)
        if stop:
            break
        if Hero_hp <= 0:
            break
        attack(3)


def attack(value,resource_id = 0):
    global Hero_hp,Orc_hp,Dragon_hp
    mutex.acquire()
    if value == 2:
        if Hero_hp > 0:
            Hero_hp -= Orc_damage
            print("Orc damaged Hero for 1 HP")
        else:
            print("Hero already killed!!!")
    elif value == 3:
        if Hero_hp > 0:
            Hero_hp -= Dragon_damage
            print("Dragon damaged Hero for 3 HP")
        else:
            print("Hero already killed!!!")
    else:
        if resource_id == 2:
            if Orc_hp > 0:
                Orc_hp -= Hero_damage		
                print("Hero damaged Orc for 2 HP")
            else:
                print("Orc already killed!!!")
        else:
            if Dragon_hp > 0:
                Dragon_hp -= Hero_damage
                print("Hero damaged Dragon for 2 HP")
            else:
                print("Dragon already killed!!!")

    print(f'Hero_health: {Hero_hp}\nOrc_health: {Orc_hp}\nDragon_health: {Dragon_hp}')
    mutex.release()


def start_thread():
    Orc = threading.Thread(target=Orc_process)
    Dragon = threading.Thread(target=Dradon_process)

    Orc.start()
    Dragon.start()


if __name__ == "__main__":

    Hero,Orc,Dragon = Hero_hp,Orc_hp,Dragon_hp
    
    start_thread()

    while True:
        mutex.acquire()
        if Hero_hp <= 0 or (Orc_hp <=0 and Dragon_hp <=0):
            stop = True
            if Hero_hp <= 0:
                print("GAME OVER --- MONSTERS WINS!!")
            elif Orc_hp <= 0 and Dragon_hp <= 0:
                print("GAME OVER --- HERO WINS!!")
            time.sleep(3)
            set_health(Hero,Orc,Dragon)
            user_input = input("Do you wish to play again?(Y/N)")
            if user_input == 'Y' or user_input =='y':
                stop = False
                start_thread()
            else:
                break

        mutex.release()
        
        print("GAME STARTS!!")

        user_input, timedOut = timedInput("PRESS 2 TO ATTACK ORC. PRESS 3 TO ATTACK DRAGON. PRESS q TO QUIT.")

        if timedOut:
            continue
        if user_input == 'q' or user_input == 'Q':
            stop = True
            break
        if user_input == "2":
            attack(0,2)
        elif user_input == "3":
            attack(0,3)
        else:
            pass
