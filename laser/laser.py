"""
This script exports all flat surfaces to a folder as dxf files.
The script will look for objects of which the two largest faces are equally large, these are usually flat surfaces intended for laser cutting.
It will export the files with names on the format componentName_bodyName_Nx.dxf where N is the number of times that object is used in the design.
You will need to modify the output directory before using the script.
"""

output_path = "/Users/arong/fusion/output"
import adsk.core, adsk.fusion, adsk.cam, traceback
import math

# Globals
_app = adsk.core.Application.cast(None)

def run(context):
    print("Running...")
    app = adsk.core.Application.get()

    des = adsk.fusion.Design.cast(app.activeProduct)
    for comp in des.allComponents:
        for body in comp.bRepBodies:
            print(body.name)
            faceList = [x for x in body.faces if isinstance(x.geometry, adsk.core.Plane)]
            faceList.sort(key=lambda face: face.area, reverse=True)
            if len(faceList) < 2:
                print("Weird body with less than 2 planar faces (" + comp.name + "/" + body.name + ")")
                continue

            a, b = faceList[0], faceList[1]
            if a.area - b.area > 0.01:
                print("Two largest faces don't seem to be of the same size. Probably not a part intended for laser cutting (" + str(a.area) + " " + str(b.area) + ") (" + comp.name + "/" + body.name + ")")
                continue

            sketch = comp.sketches.add(a)
            sketch.saveAsDXF(output_path + "/" + str(comp.name) + "_" + body.name + "_" + str(len(des.rootComponent.allOccurrencesByComponent(comp))) + "x.dxf")
            sketch.deleteMe()
            #adsk.doEvents()
    print("Done.")
