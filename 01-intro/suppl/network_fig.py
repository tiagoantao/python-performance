import svgwrite
from svgwrite.mixins import Transform

dwg = svgwrite.Drawing('01-network.svg', debug=True)

dwg.add(dwg.line(start=(300, 60), end=(300, 110), stroke='black'))
dwg.add(dwg.line(start=(290, 100), end=(300, 110), stroke='black'))
dwg.add(dwg.line(start=(310, 100), end=(300, 110), stroke='black'))
dwg.add(dwg.text('API calls over the network', insert=(310, 85), style="font-style:normal;font-weight:normal;font-size:106x;text-anchor:left;dominant-baseline:top;"))

dwg.add(dwg.rect(insert=(200, 0), size=(200, 25), fill='white', stroke='black'))
dwg.add(dwg.text('Your Python code', insert=(300, 20), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.rect(insert=(200, 25), size=(200, 25), fill='white', stroke='black'))
dwg.add(dwg.text('Python libraries', insert=(300, 45), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.add(dwg.rect(insert=(10, 120), size=(580, 50), fill='white', stroke='black'))
dwg.add(dwg.text('SMTP, IMAP,', insert=(80, 140), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('FTP, SSH, ...', insert=(80, 160), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.add(dwg.rect(insert=(150, 120), size=(80, 50), fill='white', stroke='black'))
dwg.add(dwg.text('socket', insert=(187, 150), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.add(dwg.rect(insert=(225, 120), size=(70, 50), fill='white', stroke='black'))
dwg.add(dwg.text('HTTP', insert=(261, 140), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('v1, v2', insert=(261, 160), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.rect(insert=(305, 120), size=(100, 50), fill='white', stroke='black'))

dwg.add(dwg.text('HTTP/3', insert=(350, 140), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('...', insert=(350, 160), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.add(dwg.text('DNS, DHCP,', insert=(500, 140), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('LDAP, SNMP, ...', insert=(500, 160), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))


dwg.add(dwg.rect(insert=(305, 170), size=(100, 50), fill='white', stroke='black'))
dwg.add(dwg.text('QUIC', insert=(350, 200), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))


dwg.add(dwg.rect(insert=(10, 220), size=(580, 50), fill='white', stroke='black'))
dwg.add(dwg.text('Transmission Control', insert=(150, 240), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('Protocol -- TCP', insert=(150, 260), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('User Datagram', insert=(450, 240), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('Protocol -- UDP', insert=(450, 260), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))


dwg.add(dwg.rect(insert=(10, 270), size=(580, 50), fill='white', stroke='black'))
dwg.add(dwg.text('Internet Protocol -- IP', insert=(300, 290), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('v4 and v6', insert=(300, 310), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

ns = dwg.text('Network stack', insert=(0, 0), transform="rotate(90 0 0) translate(220 -600)", style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top")
dwg.add(ns)


dwg.add(dwg.text('Local Network', insert=(300, 360), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))



dwg.add(dwg.text('Internet', insert=(600 / 2, 400), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))



dwg.add(dwg.rect(insert=(295, 120), size=(10, 150), fill='none', stroke='black'))



dwg.save()
