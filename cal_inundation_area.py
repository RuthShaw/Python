# -*- coding: utf-8 -*-

## calculate flood area using ArcPy
# Import arcpy module
import arcpy
from arcpy.sa import *

arcpy.env.workspace = r"F:\example"

# Local variables:
inFeatures = "coast.shp"
comb2 = "comb21.tif"
a = "a.shp"
b = "b.shp"
c = "c.tif"
d = "d.tif"
dR = "dReclassify.tif"
e = "e.shp"
elyr = r"F:\example\elyr.lyr"
f = "f.shp"
f1 = "f1.shp"
g = "g.shp"
gg = "gg.shp"


Input_true_raster_or_constant_value = "1"
Input_false_raster_or_constant_value = "0"

# Process: Iterate Row Selection
cursor = arcpy.UpdateCursor(inFeatures)
n = 0
arcpy.Delete_management(g, "")
#arcpy.Delete_management(g, "")
for row in cursor:
    arcpy.Delete_management(a, "")

    arcpy.Delete_management(c, "")
    arcpy.Delete_management(d, "")
    arcpy.Delete_management(e, "")
    arcpy.Delete_management(f, "")
    arcpy.Delete_management(f1, "")
    arcpy.Delete_management(b, "")
    arcpy.Delete_management(elyr, "")
    arcpy.Delete_management(dR, "")
    print n

    bainian = row.getValue("rp00100")

    # Process: Select
    arcpy.Select_analysis(inFeatures, a, 'FID = %d' % n)

    # Process: Buffer
    arcpy.Buffer_analysis(a, b, "2 DecimalDegrees", "FULL", "ROUND", "NONE", "", "PLANAR")

    # Process: Extract by Mask
    arcpy.gp.ExtractByMask_sa(comb2, b, c)

    # Process: Con
    arcpy.gp.Con_sa(c, Input_true_raster_or_constant_value, d, Input_false_raster_or_constant_value,
                    "Value <= %f" % bainian)

    # Execute Reclassify
    dReclassify = Reclassify(d, "Value", RemapRange([[1, 1]]), "NODATA")

    # Save the output
    dReclassify.save(dR)

    # Execute RasterToPolygon
    arcpy.RasterToPolygon_conversion(dR, e, "NO_SIMPLIFY", "VALUE")

    # First, make a layer from the feature class
    arcpy.MakeFeatureLayer_management(e, elyr, "", "", "#")

    # Process: Select Layer By Location
    arcpy.SelectLayerByLocation_management(elyr, "INTERSECT", a, "", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CopyFeatures_management(elyr, f)

    # Add Field & Value
    arcpy.AddField_management(f, 'rp00100', "DOUBLE")
    cursor2 = arcpy.UpdateCursor(f)
    for row2 in cursor2:
        #print(bainian)
        row2.setValue("rp00100", bainian)
        cursor2.updateRow(row2)

    #Process: Union
    # append
    if n == 0:
        # g = f
        arcpy.CopyFeatures_management(f, g)
    else:
        arcpy.Union_analysis([f,g], f1, "ALL", "", "GAPS")

        arcpy.CalculateField_management(f1, "rp00100", "max( !rp00100! , !rp00100_1! )", "PYTHON_9.3", "")

        arcpy.Delete_management(g, "")

        # Process: Dissolve
        arcpy.Dissolve_management(f1, g, ["Id","rp00100"], "", "MULTI_PART", "DISSOLVE_LINES")



    n = n + 1
    # Delete (3)


