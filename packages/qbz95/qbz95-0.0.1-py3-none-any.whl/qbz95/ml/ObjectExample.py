

class Parent:
    parentAttr = 100

    def __init__(self):
        print("parent __init__")

    def parentMethod(self):
        print('parentMethod')

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print("parent getAttr :", Parent.parentAttr)

    def myMethod(self):
        print('parent myMethod')


class Child(Parent):

    def __init__(self):
        print("child ")

    def childMethod(self):
        print ('childMethod')

    def myMethod(self):
        print ('child myMethod')


def testInherit():
    c = Child()
    c.childMethod()
    c.parentMethod()
    c.setAttr(200)
    c.getAttr()
    c.myMethod()


if __name__ == "__main__":
    testInherit()
    pass
