class Player:
  def __init__(self,connection,address,teamName="Defualt",thread=None,flag=True):
    self.connection = connection
    self.address = address
    self.teamName = teamName
    self.thread = thread
    self.flag = flag
    self.score = 0 


  
  