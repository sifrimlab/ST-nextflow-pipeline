import SimpleITK as sitk



def calculateTransform(fixed, moving):
    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
    R.SetInterpolator(sitk.sitkLinear)
    outTx = R.Execute(fixed, moving)
    return outTx

def warpImage(image, transform):
    resampled = sitk.Resample(image, transform, sitk.sitkLinear, 0.0, sitk.sitkUInt16)
    return resampled