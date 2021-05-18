import SimpleITK as sitk
import sys
import os
import re

##parse arguments
reference = sys.argv[1] 
target=sys.argv[2]
# output_dir=sys.argv[3]

prefix = os.path.splitext(target)[0]

## If it's the global first registration step, we want to add the round label to it

fixed = sitk.ReadImage(reference, sitk.sitkFloat32)
moving = sitk.ReadImage(target, sitk.sitkFloat32)

transformDomainMeshSize = [8] * moving.GetDimension()
outTx = sitk.BSplineTransformInitializer(fixed,
                                      transformDomainMeshSize)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsCorrelation()

R.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                       numberOfIterations=100,
                       maximumNumberOfCorrections=5,
                       maximumNumberOfFunctionEvaluations=1000,
                       costFunctionConvergenceFactor=1e+7)
R.SetInitialTransform(outTx, True)
R.SetInterpolator(sitk.sitkLinear)
outTx = R.Execute(fixed, moving)

resampled = sitk.Resample(moving, outTx, sitk.sitkLinear, 0.0, sitk.sitkUInt16)
sitk.WriteImage(resampled, f"{prefix}_registered.tif")
