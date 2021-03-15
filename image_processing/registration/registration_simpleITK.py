import SimpleITK as sitk
import sys
import os


def register_simpleITK(ref: str, target: str, round: int, channel: int, output_dir: str = ""):
    fixed = sitk.ReadImage(ref, sitk.sitkFloat32)

    moving = sitk.ReadImage(target, sitk.sitkFloat32)

    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
    R.SetInterpolator(sitk.sitkLinear)

    outTx = R.Execute(fixed, moving)

    print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
    print(f" Iteration: {R.GetOptimizerIteration()}")
    print(f" Metric value: {R.GetMetricValue()}")

    sitk.WriteTransform(outTx, f"{output_dir}transform_r{round}_c{channel}.txt")


    ## important commands for future transform use:
    #sitk.WriteImage(moving_resampled, outputFileName)
    #read_result = sitk.ReadTransform('euler2D.tfm')
    #moving_resampled = sitk.Resample(moving, fixed, result, sitk.sitkLinear, 0.0, moving.GetPixelID())


register_simpleITK("/media/tool/starfish_test_data/ExampleInSituSequencing/DO/REF.TIF","/media/tool/starfish_test_data/ExampleInSituSequencing/Round2/c5.TIF", 2 , 5)