import io

from os.path import exists
from os.path import splitext
from kivy.app import App
from kivy.uix.boxlayout import *
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

from v3_tools import *
from excel_integration import *


# This should not be all one class. I cannot figure out how to break it up into multiple
class snmpXL(App):
    def build(self):
        #These dictionaries will be used to convert the values in the dropdowns
        #to the strings used by pySNMP to identify them
        self.authProtocols = {
        'None' : usmNoAuthProtocol,
        'MD5' : usmHMACMD5AuthProtocol,
        'SHAv1' : usmHMACSHAAuthProtocol,
        'SHAv2 224bit' : usmHMAC128SHA224AuthProtocol,
        'SHAv2 256bit' : usmHMAC192SHA256AuthProtocol,
        'SHAv2 384bit' : usmHMAC256SHA384AuthProtocol,
        'SHAv2 512bit' : usmHMAC384SHA512AuthProtocol
        }

        self.privProtocols = {
        'None' : usmNoPrivProtocol,
        'DES' : usmDESPrivProtocol,
        '3DES' : usm3DESEDEPrivProtocol,
        'AES 128bit' : usmAesCfb128Protocol,
        'AES 192bit' : usmAesCfb192Protocol,
        'AES 256bit' : usmAesCfb256Protocol
        }

        #The file extensions accepted by openpyxl.
        #Used for error checking later.
        self.acceptableExtensions = {
            '.xlsx', '.xlsm', '.xltx', '.xltm'
        }
        #Sets the background to white
        Window.clearcolor = (1, 1, 1, 1)

        #Layout that all widgets get added to
        parent = BoxLayout(orientation='vertical', spacing = 30, padding = 15)

        #The logo. Images don't anti-alias nicely, even with an EffectWidget
        #Text is much preferable
        self.logo = Label(
            text = 'snmpXL', 
            outline_color = (.384, 0, .933),
            outline_width = 1, 
            italic = True, 
            bold = True, 
            font_size = 30,
            size_hint_y = None,
            height = 10
            )

        # #The dropdown for selecting the authentication protocol
        self.authSpinner = Spinner(
            text = "Select Authentication Protocol",
            values =("None", "MD5", "SHAv1", "SHAv2 224bit","SHAv2 256bit",
                "SHAv2 384bit", "SHAv2 512bit"),
            size_hint_y = None,
            height = 30
            )

        #The dropdown for selecting the encryption (priv) protocol
        self.privSpinner = Spinner(
            text = "Select Encryption Protocol",
            values = ("None", "DES", "3DES", "AES 128bit","AES 192bit", "AES 256bit"),
            size_hint_y = None,
            height = 30
            )

        #Declare all of the text fields users will enter data into
        self.fileLocation = TextInput(
            multiline = False, 
            hint_text = 'Enter the file location of your spreadsheet, including the file extension',
            size_hint_y = None,
            height = 30
            )
        
        self.username = TextInput(
            multiline = False, 
            hint_text = 'Enter the username used for SNMP authentication',
            size_hint_y = None,
            height = 30
            )

        self.authPass = TextInput(
            multiline = False, 
            hint_text = 'Enter the authentication password',
            password = True,
            size_hint_y = None,
            height = 30
            )    

        self.privPass = TextInput(multiline = False, 
            hint_text = 'Enter the privilege password',
            password = True,
            size_hint_y = None,
            height = 30
            )  
       
        #The button that executes the program
        runButton = Button(
            text = 'Run',
            background_color= (.384, 0, .933),
            background_normal = '',
            size_hint_y = None,
            height = 30
            )
        runButton.bind(on_release= self.callSNMP)

        #This label is what passes for text output in this cursed library
        self.textOutput = Label(
            text = 'Ready to output',
            color = (.384, 0, .933),
            size_hint_y = None, 
            height = 120
            )

        attribution = Label(
            text = 'A tool by JD Black (c) 2022, Licensed under GNU GPL3' 
                +'\nThis is free software, and you are welcome to redistribute it',
            color = (0, 0, 0), 
            font_size = 10,
            size_hint_y = None,
            height = 10
            )

        #Add everything to the layout
        parent.add_widget(self.logo)
        parent.add_widget(self.authSpinner)
        parent.add_widget(self.privSpinner)
        parent.add_widget(self.fileLocation)
        parent.add_widget(self.username)
        parent.add_widget(self.authPass)
        parent.add_widget(self.privPass)
        parent.add_widget(runButton)
        parent.add_widget(self.textOutput)
        parent.add_widget(attribution)
        
        return parent

    #Adds text to text output label with newline
    def addToLabel(self, text):
        self.textOutput.text = self.textOutput.text + '\n' + text

    def callSNMP(self, runButton = None):
        #Converts human-readable protocol names into the values used by pySNMP
        #using dictionaries defined at top
        authProtocolString = self.authProtocols.get(self.authSpinner.text)
        privProtocolString = self.privProtocols.get(self.privSpinner.text)
        
        #Clear our text output label
        self.textOutput.text = ''

        #We're going to some hacky programming due to a lack of foresight
        #Basically we're going to change the standard output, get what's printed, then put everything back
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        #This boolean will show if a restart is needed after call
        hasError = False

        #Check if the file location exists, check if file extension is
        #one of the extensions openpyxl accepts 
        name, extension = splitext(self.fileLocation.text)
        if exists(self.fileLocation.text) and (extension in self.acceptableExtensions):
            try:
            #Makes call to v3_tools
                getBulkv3(self.fileLocation.text, 
                authProtocolString, privProtocolString, self.username.text,
                self.authPass.text, self.privPass.text)
            except ValueError as err:
                print('Error: {0}, {1}'.format(err.args[0], err.args[1]))
                hasError = True
            except TypeError as err:
                print('Error: Required parameter not defined')
                hasError = True
            except:
                print('Error: Generic SNMP Error')
                hasError = True
                
        else:
            self.addToLabel('Error: File does not exist or is not of type xlsx, xltx, xlsm, or xltm')
            hasError = True

        #Grab everything that was printed to stdout
        whatWasPrinted = buffer.getvalue()
        self.addToLabel(whatWasPrinted)


        #Put stdout back, as is best practice
        sys.stdout = old_stdout

        #If there's an error, we restart automatically
        if hasError:
            self.restartWithText(5)
        else:
            #We still want to restart tool on program success
            self.restartWithText(20)
    
    #Calls the other two methods with the proper timing
    def restartWithText(self, dt):
        #Scheduler needs to be used to force the text to refresh
        Clock.schedule_once(self.addRestartText)
        Clock.schedule_once(self.resizeLabel)
        Clock.schedule_once(self.restart, dt)

    #Broken out into separate method so it can be scheduled 
    def addRestartText(self, dt):
        self.addToLabel("Restarting shortly...")

    #Reloads the app when errors are encountered
    def restart(self, dt = None):
        self.root.clear_widgets()
        self.stop()
        return snmpXL().run()
    
    #When text is output, calling this method resizes the text output to fit
    def resizeLabel(self, dt = None):
        self.textOutput.texture_update()
        self.textOutput.height = max(self.textOutput.texture_size[1], self.textOutput.height)

if __name__ == '__main__':
    Window.top = 50
    Window.size = (800, 750)
    snmpXL().run()