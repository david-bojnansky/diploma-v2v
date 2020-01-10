from tkinter import *

class Gui(Frame):   
    _ipLabel = None
    _brandLabel = None
    _modelLabel = None
    _vrnLabel = None
    _rotatesLabel = None
    _gearLabel = None
    _directionLabel = None
    _speedLabel = None
    _actionLabel = None
    _afterId = None
    
    def __init__(self, master, vehicle, foreignVehicles):
        Frame.__init__(self, master)
        self._master = master
        self._vehicle = vehicle
        self._foreignVehicles = foreignVehicles
        self._foreignVehicleLabels = []
        
        
    def _createLabel(self, table, name, title, row, col):
        l = Label(table, text=title)
        l.grid(row=row, column=col * 2, sticky=E)
        
        l = Label(table, text="Zisťujem...")
        l.grid(row=row, column=(col * 2) + 1,
               sticky=W, padx=(10, 50))
        
        setattr(self, name + "Label", l)
        
    
    def _createMyVehicleView(self):
        t = Frame(master=self._master)
        t.grid(row=0, column=0, sticky=W)
        
        self._createLabel(t, "_ip", "IP", 0, 0)
        self._createLabel(t, "_brand", "Značka", 1, 0)
        self._createLabel(t, "_model", "Model", 2, 0)
        self._createLabel(t, "_vrn", "EČV", 3, 0)
        self._createLabel(t, "_rotates", "Otáčky (o/m)", 0, 1)
        self._createLabel(t, "_gear", "Prevod", 1, 1)
        self._createLabel(t, "_direction", "Smer", 2, 1)
        self._createLabel(t, "_speed", "Rýchlosť (km/h)", 3, 1)
        self._createLabel(t, "_action", "Činnosť", 4, 1)
        
        
    def _createForeignVehiclesView(self):
        table = Frame(master=self._master)
        table.grid(row=1, column=0, sticky=W)
        
        titles = ["#", "IP", "Značka", "Model", "EČV",
                  "Smer", "Rýchlosť (km/h)", "Činnosť"]
        
        l = Label(table, text="VOZIDLÁ V DOSAHU")
        l.grid(row=0, column=0,
               columnspan=len(titles),
               pady=(20, 10))

        for i, t in enumerate(titles):
            l = Label(table, text=t)
            l.grid(row=1, column=i, sticky=W, padx=(0, 10))
        
        for i in range(5):
            self._foreignVehicleLabels.append([])
            
            for j in range(len(titles)):
                l = Label(table)
                l.grid(row=i + 2, column=j,
                       sticky=W, padx=(0, 10))
                self._foreignVehicleLabels[i].append(l)
                
                
    def updateMyVehicle(self):
        self._ipLabel["text"] = self._vehicle.echo("ip")
        self._brandLabel["text"] = self._vehicle.echo("brand")
        self._modelLabel["text"] = self._vehicle.echo("model")
        self._vrnLabel["text"] = self._vehicle.echo("vrn")
        self._rotatesLabel["text"] = self._vehicle.echo("rotates")
        self._gearLabel["text"] = self._vehicle.echo("gear")
        self._directionLabel["text"] = self._vehicle.echo("directionAsText")
        self._speedLabel["text"] = self._vehicle.echo("speed")
        self._actionLabel["text"] = self._vehicle.echo("actionAsText")
    
    
    def updateForeignVehicles(self):
        for i, row in enumerate(self._foreignVehicleLabels):
            row[0]["text"] = str(i + 1) + "."
            
            if i < len(self._foreignVehicles):
                v = self._foreignVehicles[i]
                
                row[1]["text"] = v.echo("ip")
                row[2]["text"] = v.echo("brand")
                row[3]["text"] = v.echo("model")
                row[4]["text"] = v.echo("vrn")
                row[5]["text"] = v.echo("directionAsText")
                row[6]["text"] = v.echo("speed")
                row[7]["text"] = v.echo("actionAsText")
            else:
                for j in range(7):
                   row[j + 1]["text"] = ""
                
    
    def invokeLater(self, runner):
        self._afterId = self.after(200, runner)
                
                
    def show(self, invokeLaterRunner):
        self._master.title("V2V komunikácia použitím minipočítača Raspberry Pi - Diplomová práca (c) 2020 Bojnanský Dávid")
        self._master.resizable(True, False)
        self._createMyVehicleView()
        self._createForeignVehiclesView()
        self.invokeLater(invokeLaterRunner)  
        self._master.mainloop()
                
                
    def close(self):
        if self._afterId != None:
            self.after_cancel(self._afterId)
            
        self._master.quit()
        