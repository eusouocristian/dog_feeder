# Dog Feeder Project

This project solves a problem when it is necessary to stay away from home for long periods, such as weekends and holidays.
Clone the repository into your home directory and run using python 3.7+.
Design:

![Imagem](/static/design.png)

The motor datasheet can be found [here](https://ecksteinimg.de/Datasheet/Schrittmotor/JK42HS40-1004A/JK42HS40-1004AC.pdf).

The A4988 Driver datasheet can be found [here](https://pdf1.alldatasheet.com/datasheet-pdf/view/338780/ALLEGRO/A4988.html).

In this project I used the full step configuration as mentioned at the driver's documentation:

![image](/static/microsteps.png)

Using the GUI, it is possible to schedule three programs for automatic feeding and speed/time adjustments. Let's se it in action (automatic):

![image](/static/dog_feeder_gui1.png)


A start/stop buttons can also be used to manually use the feeder. All programs are maintained in a Sqlite databank. There is a button to register the program into the dataabe. The last registered program remain active for the next app launch.S

![image](/static/dog_feeder_gui2.png)

Instructions to handle autostarting this project on a Raspberry Pi (Raspbian):
Install xtem:

    sudo apt install xterm

Create a desktop file:

    mkdir -p ~/.config/autostart/dog_feeder.desktop

Content:

    [Desktop Entry]
    Type=Application
    Name=Dog Feeder
    Exec=xterm -hold -e '/usr/bin/python3 /home/pi/dog_feeder/dog_feeder.py'

