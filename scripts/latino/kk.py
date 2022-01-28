import re

fullMassPoint = re.match(r"([a-zA-Z]+)([0-9]+)", "pseudo500")
mediatorSelected = fullMassPoint.group(1)
massPointSelected = fullMassPoint.group(2)
print(mediatorSelected)
print(massPointSelected)
