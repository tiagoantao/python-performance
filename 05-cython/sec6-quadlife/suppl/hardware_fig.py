import svgwrite


dwg = svgwrite.Drawing('01-hardware.svg', debug=True)

dwg.add(dwg.text('Hardware Ecology', insert=(0, 30), style="font-style:normal;font-weight:normal;font-size:20px;"))

dwg.add(dwg.rect(insert=(150, 60), size=(300, 40), fill='white', stroke='black'))
dwg.add(dwg.text('On-premises / Cloud / Hybrid', insert=(300, 80), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:middle;"))


dwg.add(dwg.rect(insert=(10, 100), size=(580, 210), fill='white', stroke='black'))
dwg.add(dwg.line(start=(10 + 580 / 3, 100), end=(10 + 580 / 3, 310), stroke='black'))
dwg.add(dwg.line(start=(10 + 580 / 1.5, 100), end=(10 + 580 / 1.5, 280), stroke='black'))


dwg.add(dwg.text('Computing', insert=(10 + 580 / 6, 120), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))


dwg.add(dwg.text('Metal', insert=(15, 150), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('VM', insert=(15, 170), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Cloud instance', insert=(15, 190), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Serverless', insert=(15, 210), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))



dwg.add(dwg.text('Storage', insert=(10 + 580 / 2, 120), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.add(dwg.text('CPU Cache', insert=(15 + 580 / 3, 150), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('RAM', insert=(15 + 580 / 3, 170), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('File System', insert=(15 + 580 / 3, 190), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('SQL', insert=(15 + 580 / 3, 210), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('NoSQL', insert=(15 + 580 / 3, 230), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Cloud proprietary', insert=(15 + 580 / 3, 250), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))



dwg.add(dwg.text('Network', insert=(10 + 580 / 1.2, 120), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))
dwg.add(dwg.text('Topology', insert=(15 + 580 / 1.5, 150), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Protocols', insert=(15 + 580 / 1.5, 170), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Speed', insert=(15 + 580 / 1.5, 190), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))
dwg.add(dwg.text('Latency', insert=(15 + 580 / 1.5, 210), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:right;dominant-baseline:top;"))


dwg.add(dwg.text('Network Attached Storage', insert=(580 / 1.5, 300), style="font-style:normal;font-weight:normal;font-size:20px;text-anchor:middle;dominant-baseline:top;"))

dwg.save()
