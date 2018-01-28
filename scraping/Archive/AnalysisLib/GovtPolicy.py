class GovtPolicy:
    def __init__(self, _name):
        self.name = _name
        self.scale1 = 0
        self.scale2 = 0
        self.scale3 = 0
        self.scale4 = 0
        self.scale5 = 0
    
    def getName(self):
        return self.name
    
    def getScale(self):
        return [self.scale1, self.scale2, self.scale3, self.scale4, self.scale5]
    
    def increScale1(self):
        self.scale1 += 1
    
    def increScale2(self):
        self.scale2 += 1
    
    def increScale3(self):
        self.scale3 += 1
        
    def increScale4(self):
        self.scale4 += 1
        
    def increScale5(self):
        self.scale5 += 1

def instantObject(Name):
    return GovtPolicy(Name)
