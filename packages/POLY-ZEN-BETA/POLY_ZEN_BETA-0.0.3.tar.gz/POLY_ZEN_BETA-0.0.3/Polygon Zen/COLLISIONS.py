def IfCollide(self,Others,px=1):
            if Others.x <= self.x + self.width and Others.x >= self.x + self.width  and Others.y >= self.y and Others.y <= self.y + self.height or Others.x  <= self.x + 1 + self.width and Others.x >= self.x and Others.y + Others.height >= self.y and Others.y <= self.y + self.height:
                Others.x += px
            if Others.x + Others.width >= self.x and Others.x + Others.width <= self.x + self.width - 1 and Others.y + Others.height >= self.y and Others.y <= self.y + self.height:
                Others.x -= px
            if Others.y <= self.y + self.height + 1 and Others.y >= self.y + self.height + 1 and Others.x >= self.x and Others.x <= self.x + self.width or Others.y + Others.height <= self.y + 1 + self.height and Others.y >= self.y and Others.x + 20 >= self.x and Others.x <= self.x + self.width:
                Others.y += px
            if Others.y + Others.height >= self.y and Others.y + Others.height <= self.y + self.height - 2 and Others.x + Others.width >= self.x and Others.x <= self.x + self.width:
                Others.y -= px
            #return True
def IfEnter(self,Others):
            if Others.x <= self.x + self.width and Others.x >= self.x + self.width  and Others.y >= self.y and Others.y <= self.y + self.height or Others.x  <= self.x + 1 + self.width and Others.x >= self.x and Others.y + Others.height >= self.y and Others.y <= self.y + self.height:
                return True
            if Others.x + Others.width >= self.x and Others.x + Others.width <= self.x + self.width - 1 and Others.y + Others.height >= self.y and Others.y <= self.y + self.height:
                return True
            if Others.y <= self.y + self.height + 1 and Others.y >= self.y + self.height + 1 and Others.x >= self.x and Others.x <= self.x + self.width or Others.y + Others.height <= self.y + 1 + self.height and Others.y >= self.y and Others.x + 20 >= self.x and Others.x <= self.x + self.width:
                return True
            if Others.y + Others.height >= self.y and Others.y + Others.height <= self.y + self.height - 2 and Others.x + Others.width >= self.x and Others.x <= self.x + self.width:
                return True 