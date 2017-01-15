import wx
import os
from BMAPI import *
from IDBClient import *
class MainConsole(wx.Frame):

    lowBattery = False

    def __init__(self, *args, **kw):
        super(MainConsole, self).__init__(*args, **kw)
        self.api = BMAPI()
        self.resultsObjectsToDisplay = []
        self.InitIDB()
        self.InitUI()

    def InitIDB(self):
        self.idbc = IDBClient()


    def InitUI(self):
        self.pnl = wx.Panel(self)
        self.createMainMenu()
        self.SetSize((600, 800))
        self.SetTitle('MainMenu')
        self.Centre()
        self.Show(True)

    def createMainMenu(self):
        settingButton = wx.Button(self.pnl, label='Settings', pos=(20, 30))
        settingButton.Bind(wx.EVT_BUTTON, self.OnSettings)
        navigationButton = wx.Button(self.pnl, label='Navigation', pos=(20, 60))
        navigationButton.Bind(wx.EVT_BUTTON, self.OnNavigation)
        #driveControllerButton = wx.Button(self.pnl, label="Drive", pos=(20, 90))
        #driveControllerButton.Bind(wx.EVT_BUTTON, self.OnDriveContr)

    def OnDriveContr(self, e):
        self.clearScreen()
        self.createDriveControllerMenu()

    def OnNavigation(self, e):
        self.clearScreen()
        self.createNavigationMenu()

    def OnSettings(self, e):
        self.clearScreen()
        self.createSettingsMenu()

    def OnBack(self, e):
        self.clearScreen()
        self.createMainMenu()

    def createChairsSettings(self):
        self.mirrorsLabel = wx.StaticText(self.pnl, label='Chairs settings', pos=(5, 110))
        self.chairAutomaticSetPositionDueUserSettings = wx.CheckBox(self.pnl, label='Automatic set position base on user settings', pos=(20, 130))
        self.chairsAutomaticHeatWhenTempIsLow = wx.CheckBox(self.pnl, label='Automatic turn on heating when temperature is lower than set degres', pos=(20, 150))
        self.chairsAutomaticHeatWhenTempIsLow.Bind(wx.EVT_CHECKBOX, self.OnChairCheckBoxTempVisible)

    def OnChairCheckBoxTempVisible(self, e):
        if self.chairsAutomaticHeatWhenTempIsLow.GetValue():
            self.minTempToChairHeating = wx.TextCtrl(self.pnl,  value='0', pos=(20, 170))
            self.pnl.Refresh()
        else:
            self.minTempToChairHeating.Destroy()
            self.pnl.Refresh()

    def createSettingsMenu(self):
        self.createMirrorsSettings()
        self.createChairsSettings()
        self.backToMainMenu = wx.Button(self.pnl, label='Back', pos=(500, 700))
        self.backToMainMenu.Bind(wx.EVT_BUTTON, self.OnBack)

    def createNavigationMenu(self):
        self.SetTitle("Navigation")
        self.sourceLabel = wx.StaticText(self.pnl, label="Starting point", pos=(0, 20))
        self.sourceText = wx.TextCtrl(self.pnl, value="Wroclaw", pos=(150, 20))
        self.secondTargetLabel = wx.StaticText(self.pnl, label="First target", pos=(0, 50))
        self.secondTarget = wx.TextCtrl(self.pnl, value="Krakow", pos=(150,50))
        self.thirdTargetLabel = wx.StaticText(self.pnl, label="Second point", pos=(0, 80))
        self.thirdTarget = wx.TextCtrl(self.pnl, value="Berlin", pos=(150,80))
        self.fourthTargetLabel = wx.StaticText(self.pnl, label="Third point", pos=(0, 110))
        self.fourthTarget = wx.TextCtrl(self.pnl, value="Paris", pos=(150,110))
        self.fifthTargetLabel = wx.StaticText(self.pnl, label="Target", pos=(0, 140))
        self.fifthTarget = wx.TextCtrl(self.pnl, value="Madrid", pos=(150,140))
        self.constrainType = wx.CheckBox(self.pnl, label="Max fuel cost", pos=(20, 170))
        self.constrainValue = wx.TextCtrl(self.pnl, pos=(20, 190))
        navigateButton = wx.Button(self.pnl, label="Designate", pos=(20, 280))
        navigateButton.Bind(wx.EVT_BUTTON, self.OnNavigate)
        self.Refresh()

    def createDriveControllerMenu(self):
        self.eco = wx.Button(self.pnl, label="ECO", pos=(20, 20))
        #self.eco.Bind(wx.EVT_BUTTON, self.OnDriveType)
        self.comfort = wx.Button(self.pnl, label="COMFORT", pos=(110, 20))
        #self.comfort.Bind(wx.EVT_BUTTON, self.OnDriveType)
        self.normal = wx.Button(self.pnl, label="NORMAL", pos=(200, 20))
        #self.normal.Bind(wx.EVT_BUTTON, self.OnDriveType)
        self.sport = wx.Button(self.pnl, label="SPORT", pos=(290, 20))
        #self.sport.Bind(wx.EVT_BUTTON, self.OnDriveType)
        self.individual = wx.Button(self.pnl, label="CUSTOM", pos=(380, 20))
        #self.individual.Bind(wx.EVT_BUTTON, self.OnDriveType)
        self.offroad = wx.Button(self.pnl, label="OFFROAD", pos=(470, 20))
        #self.offroad.Bind(wx.EVT_BUTTON, self.OnDriveType)

    def OnDriveType(self, e):
        selectedType = e.GetEventObject().GetLabel()
        self.idbc.sendRequest("0x1-MANCONSOLE-CAR/DRIVE_TYPE_CHANGE_REQ")
        self.idbc.sendRequest("0x6-MAINCONSOLE-CAR/DRIVE_TYPE_CHANGE_REQ;type;"+selectedType)

    def OnNavigate(self, e):
        self.api.ifFileExistRemoveIt()
        self.prepareTopology()
        self.idbc.sendRequest("0x1-MAINCONSOLE-CAR/GPS/NAVIGATE_REQ")
        self.idbc.sendRequest("0x6-MAINCONSOLE-CAR/GPS/NAVIGATE_REQ;file;/home/mato3/OSCAR/SYS/TEMP/routes.txt")
        if self.constrainValue.GetValue() != '':
            self.idbc.sendRequest("0x1-MAINCONSOLE-CAR/GPS/CONSTRAIN")
            self.idbc.sendRequest("0x6-MAINCONSOLE-CAR/GPS/CONSTRAIN;type;"+self.constrainType.GetLabelText())
            self.idbc.sendRequest("0x6-MAINCONSOLE-CAR/GPS/CONSTRAIN;value;"+self.constrainValue.GetValue())
        if self.idbc.setObserverForObject("CAR/GPS/RESULT"):
            route = self.idbc.sendRequest("0x9-MAINCONSOLE-CAR/GPS/RESULT;selectedRoute").split("-")[2]
            routeType = self.idbc.sendRequest("0x9-MAINCONSOLE-" + route + ";type")
            routeDistance = self.idbc.sendRequest("0x9-MAINCONSOLE-" + route + ";distance")
            routeDuration = self.idbc.sendRequest("0x9-MAINCONSOLE-" + route + ";duration")
            self.neededFuel = self.idbc.sendRequest("0x9-MAINCONSOLE-" + route + ";fuelCost")
            #print "RESULT IS " + routeType
            targets = self.api.translate(routeType.split("-")[2])
            f = open("/home/mato3/OSCAR/SYS/TEMP/routes.txt", "r")
            content = f.readlines()
            self.displayResults(targets, content)

    def displayResults(self, targets, result):
        self.clearScreen()
        self.SetTitle("Navigation results")
        self.resultLabel = wx.StaticText(self.pnl, label='ROUTES RESULT', pos=(5, 5))
        self.listCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT, pos=(0, 50))
        self.listCtrl.InsertColumn(0, 'From')
        self.listCtrl.InsertColumn(1, "To")
        self.listCtrl.InsertColumn(2, "Duration")
        self.listCtrl.InsertColumn(3, "Distance")
        self.listCtrl.InsertColumn(4, "Traffic")
        duration = 0.0
        distance = 0.0
        for target in targets:
            number = self.listCtrl.GetItemCount()
            text = result[(target * 2) - 1]
            stext = text.split(";")
            self.listCtrl.InsertStringItem(number, stext[0])
            self.listCtrl.SetStringItem(number, 1, stext[1])
            self.listCtrl.SetStringItem(number, 2, stext[2])
            self.listCtrl.SetStringItem(number, 3, stext[3])
            self.listCtrl.SetStringItem(number, 4, stext[4])
            duration += float(stext[2])
            distance += float(stext[3])
        number = self.listCtrl.GetItemCount()
        self.listCtrl.InsertStringItem(number, "SUM")
        self.listCtrl.SetStringItem(number, 2, str(duration))
        self.listCtrl.SetStringItem(number, 3, str(distance))
        self.listCtrl.InsertStringItem(number + 1, "Necessary fuesl")
        self.listCtrl.SetStringItem(number + 1, 2, self.neededFuel.split("-")[2])
        self.pnl.Refresh()
        

    def prepareRequest(self, src, dest):
        self.api.setData(src, dest)
        self.api.sendRequest()
        self.api.prepareResult()
        self.api.printResults()

    def prepareTopology(self):
        print "1: \n"
        self.prepareRequest(self.sourceText.GetValue(), self.secondTarget.GetValue())	
        print "2: \n"
        self.prepareRequest(self.sourceText.GetValue(), self.thirdTarget.GetValue())
        print "3: \n"
        self.prepareRequest(self.sourceText.GetValue(), self.fourthTarget.GetValue())		#1
        print "4: \n"
        self.prepareRequest(self.sourceText.GetValue(), self.fifthTarget.GetValue())
        print "5: \n"
        self.prepareRequest(self.secondTarget.GetValue(), self.thirdTarget.GetValue()) 
        print "6: \n"
        self.prepareRequest(self.secondTarget.GetValue(), self.fourthTarget.GetValue())	#2
        print "7: \n"
        self.prepareRequest(self.secondTarget.GetValue(),  self.fifthTarget.GetValue())
        print "8: \n"
        self.prepareRequest(self.thirdTarget.GetValue(),  self.fourthTarget.GetValue())	
        print "9: \n"
        self.prepareRequest(self.thirdTarget.GetValue(),  self.fifthTarget.GetValue())	#3
        print "10: \n"
        self.prepareRequest(self.fourthTarget.GetValue(),  self.fifthTarget.GetValue())	#4

	def createRoutes(self):
		pass

    def createMirrorsSettings(self):
        self.mirrorsLabel = wx.StaticText(self.pnl, label='Mirrors settings', pos=(5, 10))
        self.mirrorDefaultClosingTick = wx.CheckBox(self.pnl, label='Automatic closing mirrors after door locked', pos=(20, 30))
        self.mirrorSetDwnOnBack = wx.CheckBox(self.pnl, label='Automatic move down mirrors when reverse shift has been activated', pos=(20, 50))
        self.mirrorDeadZoneDiode = wx.CheckBox(self.pnl, label='Dead zone diode enabled', pos=(20, 70))
        self.mirrorDeadZoneDiode.SetValue(True)
        self.mirrorAutomaticSetRegardingToChairAndBolsterPos = wx.CheckBox(self.pnl, label='Automatic set mirror due to chair and bolster position', pos=(20, 90))

    def clearScreen(self):
        for child in self.pnl.GetChildren():
            child.Destroy()
        self.pnl.Refresh()

def main():

    MainConsoleApp = wx.App()
    MainConsole(None)
    MainConsoleApp.MainLoop()



if __name__ == '__main__':
    main()
