import SimpleITK as sitk
import sys
import os

reference = sys.argv[1] 
target=sys.argv[2]
# output_dir=sys.argv[3]

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
sitk.WriteImage(resampled, "registered.tif")
# print(str(reference) + str(target))