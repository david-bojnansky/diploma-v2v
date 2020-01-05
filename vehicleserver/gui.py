from tkinter import *

class Gui(Frame):   
    ipLabel = None
    brandLabel = None
    modelLabel = None
    vrnLabel = None
    rotatesLabel = None
    gearLabel = None
    directionLabel = None
    speedLabel = None
    actionLabel = None
    afterId = None
    
    def __init__(self, master, vehicle, foreignVehicles):
        Frame.__init__(self, master)
        self.master = master
        self.vehicle = vehicle
        self.foreignVehicles = foreignVehicles
        self.foreignVehicleLabels = []
        
        
    def createLabel(self, table, name, title, row, col):
        l = Label(table, text=title)
        l.grid(row=row, column=col * 2, sticky=E)
        
        l = Label(table, text="Zisťujem...")
        l.grid(row=row, column=(col * 2) + 1,
                sticky=W, padx=(10, 50))
        
        setattr(self, name + "Label", l)
        
    
    def createMyVehicleView(self):
        table = Frame(master=self.master)
        table.grid(row=0, column=0, sticky=W)
        
        self.createLabel(table, "ip", "IP", 0, 0)
        self.createLabel(table, "brand", "Značka", 1, 0)
        self.createLabel(table, "model", "Model", 2, 0)
        self.createLabel(table, "vrn", "EČV", 3, 0)
        self.createLabel(table, "rotates", "Otáčky (o/m)", 0, 1)
        self.createLabel(table, "gear", "Prevod", 1, 1)
        self.createLabel(table, "direction", "Smer", 2, 1)
        self.createLabel(table, "speed", "Rýchlosť (km/h)", 3, 1)
        self.createLabel(table, "action", "Činnosť", 4, 1)
        
        
    def createForeignVehiclesView(self):
        table = Frame(master=self.master)
        table.grid(row=1, column=0, sticky=W)
        
        titles = ["#", "IP", "Značka", "Model", "EČV",
                  "Smer", "Rýchlosť", "Činnosť"]
        
        l = Label(table, text="VOZIDLÁ V DOSAHU")
        l.grid(row=0, column=0,
               columnspan=len(titles),
               pady=(20, 10))     

        for i, t in enumerate(titles):
            l = Label(table, text=t)
            l.grid(row=1, column=i, sticky=W, padx=(0, 10))
        
        for i in range(5):
            self.foreignVehicleLabels.append([])
            
            for j in range(len(titles)):
                l = Label(table)
                l.grid(row=i + 2, column=j, sticky=W)
                self.foreignVehicleLabels[i].append(l)
                
                
    def updateMyVehicle(self):
        self.ipLabel["text"] = self.vehicle.echo("ip")
        self.brandLabel["text"] = self.vehicle.echo("brand")
        self.modelLabel["text"] = self.vehicle.echo("model")
        self.vrnLabel["text"] = self.vehicle.echo("vrn")
        self.rotatesLabel["text"] = self.vehicle.echo("rotates")
        self.gearLabel["text"] = self.vehicle.echo("gear")
        self.directionLabel["text"] = self.vehicle.echo("directionAsText")
        self.speedLabel["text"] = self.vehicle.echo("speed")
        self.actionLabel["text"] = self.vehicle.echo("actionAsText")
    
    
    def updateForeignVehicles(self):
        for i, row in enumerate(self.foreignVehicleLabels):
            row[0]["text"] = str(i + 1) + "."
            
            if i < len(self.foreignVehicles):
                v = self.foreignVehicles[i]
                
                row[1]["text"] = v.echo("ip")
                row[2]["text"] = v.echo("brand")
                row[3]["text"] = v.echo("model")
                row[4]["text"] = v.echo("vrn")
                row[5]["text"] = v.echo("directionAsText")
                row[6]["text"] = v.echo("speed")
                row[7]["text"] = v.echo("actionAsText")
            else:
                for j in range(7):
                   row[j + 1]["text"] = None
                
    
    def invokeLater(self, runner):
        self.afterId = self.after(200, runner)
                
                
    def show(self, invokeLaterRunner):
        self.master.title("V2V Server (c) 2020 Bojnanský Dávid")
        self.master.resizable(False, False)
        #self.geometry("400x200")
        self.createMyVehicleView()
        self.createForeignVehiclesView()
        self.invokeLater(invokeLaterRunner)  
        self.master.mainloop()
                
                
    def close(self):
        if self.afterId != None:
            self.after_cancel(self.afterId)
            
        self.master.quit()
        