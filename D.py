import math

# header
print "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"
print "<!-- Created with Emacs -->"
print "<svg"
print "   xmlns:svg=\"http://www.w3.org/2000/svg\""
print "   xmlns=\"http://www.w3.org/2000/svg\""
print "   version=\"1.0\""
print "   width=\"2400\""
print "   height=\"60\">"
print "  <g>"

print "   <path"
print "       d=\"M 0.0,30 L 2400,30\""
print "       style=\"fill:none;stroke:#ffffff;stroke-width:60px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"

offset = 50
for i in range(100,200):
    ln = str(math.log(i/100.)*1000 + offset)
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        print "  <text style=\"font-size:12px;fill:#000000;\">"
        print "      <tspan"
        print "       x=\"" + str(ln) + "\""
        print "       y=\"" + h3 + "\""
        print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(float(int(i)*10/1000.)) + "</tspan></text>"
    elif int((i/5)*5) == i:
        h1 = "0"; h2 = "17";
    else:
        h1 = "0"; h2 = "15";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(200,500,2):
    ln = str(math.log(i/100.)*1000 + offset)
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(float(int(i)*10/1000.)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(500,1005,5):
    ln = str(math.log(i/100.)*1000 + offset)
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(float(int(i)*10/1000.)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"


# footer
print "  </g>"
print "</svg>"
