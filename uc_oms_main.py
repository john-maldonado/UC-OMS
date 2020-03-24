import sys
import socket

# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication
# pylint: enable=no-name-in-module

from uc_oms_ui import LoginForm, MainMenu
from uc_oms_protocol import Protocol, PCommands, OMSUser

# Define Qt App
qt_app = QApplication(sys.argv)

# Define User Instance
u = OMSUser()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.0.119", 4444))

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
s.setblocking(False)

if __name__ == "__main__":
    Exit = False
    while (not Exit):

        # Initiate Connection
        Protocol().sendConnect(s)
        s.setblocking(True)
        message = Protocol().receiveMessage(s)
        s.setblocking(False)
        if message is False:
            print('Failed to connect to server')
            input('Press Enter to continue')
        else:
            command = message.command
            if command == PCommands.connect:
                print('Connected to server!')
                # Show Login Screen
                app = LoginForm(qt_app, s, u)
                login_action = app.run()
                if login_action == 'login':
                    # Proceed to Main Menu
                    app = MainMenu(qt_app, s, u)
                    main_action = app.run()
                    if main_action == 'logout':
                        Exit = False
                    else:
                        Exit = True
                else:
                    Exit = True
