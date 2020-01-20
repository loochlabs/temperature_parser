from converter import TemperatureParser 

parser = TemperatureParser()
#parser.CreateImages()

#parser.CreateScaledImages()
parser.CreateScaledImage(parser.config["datapath"] + "/" + "Ellesmere_IR_flight01_1000ft_004341.csv", parser.config["imageScale"])
