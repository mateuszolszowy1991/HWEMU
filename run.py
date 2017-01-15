import wx


class HWEmu(wx.Frame):

    lowBattery = False

    def __init__(self, *args, **kw):
        super(HWEmu, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        pnl = wx.Panel(self)
        openButton = wx.Button(pnl, label='UnLock', pos=(20, 30))
        switchButton = wx.Button(pnl, label='Switch', pos=(40, 60))
        closeButton = wx.Button(pnl, label='Lock', pos=(20, 90))
        lowBatterySim = wx.ToggleButton(pnl, label='Low battery', pos=(20, 120))


        openButton.Bind(wx.EVT_BUTTON, self.OnOpen)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        switchButton.Bind(wx.EVT_BUTTON, self.OnSwitch)
        lowBatterySim.Bind(wx.EVT_TOGGLEBUTTON, self.OnLowBattery)

        doorOpenButton = wx.Button(pnl, label='openDoor', pos=(150, 30))
        doorCloseButton = wx.Button(pnl, label='closeDoor', pos=(150, 60))

        doorOpenButton.Bind(wx.EVT_BUTTON, self.OnDoorOpen)
        doorCloseButton.Bind(wx.EVT_BUTTON, self.OnDoorClose)

        self.SetSize((270, 200))
        self.SetTitle('wx.Button')
        self.Centre()
        self.Show(True)

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
    HWEmu(None)
    hwEmuApp.MainLoop()



if __name__ == '__main__':
    main()