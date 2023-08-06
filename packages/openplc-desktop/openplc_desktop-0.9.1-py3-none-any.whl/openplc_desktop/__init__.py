
import os
import sys

HERE_PATH =  os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE_PATH, ".."))

if not HERE_PATH in sys.path:
    sys.path.insert(0, HERE_PATH)


from Qt import QtGui, QtWidgets


class EXIT_CODE:
    restart = 10
    upgrade = 11
    crash = 99
    no_db = 98
    quit = 0


def show_splash():
    # splashImage = QtGui.QPixmap( "../images/corp/splash.png" )
    splashScreen = QtWidgets.QSplashScreen()
    splashScreen.showMessage("  Loading . . . ")
    splashScreen.show()
    return splashScreen


def start_app(appWidget, args, splash=True):
    splashScreen = None

    app = QtWidgets.QApplication(sys.argv)
    # if len(app.arguments()) == 1:
    #	print("FATAL: no database")
    #	sys.exit(EXIT_CODE.no_db)

    ## Main Window
    window = appWidget(args=args)  # launcher=launcher, debug=debug, dbserver=dbserver, full_screen=full_screen)

    # if app_globals.settings.is_dev() == False and splash== True:
    #	splashScreen.finish( window )

    window.show()

    exit_code = app.exec_()
    sys.exit(exit_code)
