import SimpleITK as sitk
import sys
import os
import re

##parse arguments
reference = sys.argv[1] 
target=sys.argv[2]
# output_dir=sys.argv[3]

prefix = os.path.splitext(target)[0]

if len(sys.argv)>3:
    round_nr = (sys.argv[3]) + "_"
else:
    round_nr=""
fixed = sitk.ReadImage(reference, sitk.sitkFloat32)
moving = sitk.ReadImage(target, sitk.sitkFloat32)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsCorrelation()
R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
R.SetInterpolator(sitk.sitkLinear)
outTx = R.Execute(fixed, moving)
# print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
# print(f"Calculating transform of round {round}, channel {channel}...")
# print(f"Finished at iteration {R.GetOptimizerIteration()} with a metric value of {R.GetMetricValue()}")
# sitk.WriteTransform(outTx, f"transform_r{round}_c{channel}.txt")
resampled = sitk.Resample(moving, outTx, sitk.sitkLinear, 0.0, moving.GetPixelID())
sitk.WriteImage(resampled, f"{round_nr}{prefix}_registered.tif")
