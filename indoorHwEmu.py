import wx


class indoorHWEmu(wx.Frame):

    lowBattery = False

    def __init__(self, *args, **kw):
        super(indoorHWEmu, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        pnl = wx.Panel(self)
        startButton = wx.Button(pnl, label="START/STOP", pos=(20, 30))
        startButton.Bind(wx.EVT_BUTTON, self.OnStart)
        #dailyButton = wx.Button(pnl, label='DAILY', pos=(20, 30))
        #positionButton = wx.Button(pnl, label='POSTION', pos=(40, 60))
        ##beamButton = wx.Button(pnl, label='BEAM', pos=(20, 90))
        ##blinkerLEFTButton = wx.Button(pnl, label='BLINKER_LEFT', pos=(20, 120))
        ##doorOpenButton = wx.Button(pnl, label='openDoor', pos=(150, 30))
        ##doorCloseButton = wx.Button(pnl, label='closeDoor', pos=(150, 60))

        #dailyButton.Bind(wx.EVT_BUTTON, self.OnDaily)
        #positionButton.Bind(wx.EVT_BUTTON, self.OnPosition)
        #beamButton.Bind(wx.EVT_BUTTON, self.OnBeam)
        #blinkerLEFTButton.Bind(wx.EVT_TOGGLEBUTTON, self.OnBlinkerLeft)



        #doorOpenButton.Bind(wx.EVT_BUTTON, self.OnDoorOpen)
        #doorCloseButton.Bind(wx.EVT_BUTTON, self.OnDoorClose)

        self.SetSize((270, 200))
        self.SetTitle('wx.Button')
        self.Centre()
        self.Show(True)

    def OnStart(self, e):
        f = open("D:/private/IDB/SYS/sigs/USER_SIG.dat", "w")
        f.write("0x51")
        f.close()
        print "START SIGNAL"

    def OnOpen(self, e):
        f = open("D:/private/IDB/SYS/sigs/RC_SIG.dat", "w")
        if not self.lowBattery:
            f.write("RC9999;120;0x1")
        else:
            f.write("RC9999;79;0x1")
        f.close()
        print "OPEN SIGNAL"

    def OnClose(self, e):
        f = open("D:/private/IDB/SYS/sigs/RC_SIG.dat", "w")
        if not self.lowBattery:
            f.write("RC9999;120;0x2")
        else:
            f.write("RC9999;79;0x2")
        f.close()
        print "OPEN SIGNAL"

    def OnSwitch(self, e):
        f = open("D:/private/IDB/SYS/sigs/RC_SIG.dat", "w")
        if not self.lowBattery:
            f.write("RC9999;120;0x3")
        else:
            f.write("RC9999;79;0x3")
        f.close()
        print "OPEN SIGNAL"

    def OnLowBattery(self,e):
        self.lowBattery = not self.lowBattery
        print "Low battery: ", self.lowBattery

    def OnDoorOpen(self, e):
        f = open("D:/private/IDB/SYS/sigs/USER_DOORS_SIG.dat", "w")
        f.write("FRONT_LEFT;Opened")
        f.close()
        print "Door opened"

    def OnDoorClose(self, e):
        f = open("D:/private/IDB/SYS/sigs/USER_DOORS_SIG.dat", "w")
        f.write("FRONT_LEFT;Closed")
        f.close()
        print "Door closed"

def main():

    hwEmuApp = wx.App()
    indoorHWEmu(None)
    hwEmuApp.MainLoop()



if __name__ == '__main__':
    main()