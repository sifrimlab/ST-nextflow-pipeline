import SimpleITK as sitk
import sys
import os

ref = "/home/nacho/Documents/Code/starfish/image_similarity/imgs/ref_tile48.tif"
target = "/home/nacho/Documents/Code/starfish/image_similarity/imgs/r1_c2_tile48.tif"

def register_simpleITK(ref, target):
    def command_iteration(method):
        print(f"{method.GetOptimizerIteration():3} = {method.GetMetricValue():10.5f} : {method.GetOptimizerPosition()}")


    # if len(sys.argv) < 4:
    #     print("Usage:", sys.argv[0], "<fixedImageFilter> <movingImageFile>",
    #           "<outputTransformFile>")
    #     sys.exit(1)

    fixed = sitk.ReadImage(ref, sitk.sitkFloat32)

    moving = sitk.ReadImage(target, sitk.sitkFloat32)

    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
    R.SetInterpolator(sitk.sitkLinear)

    R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R))

    outTx = R.Execute(fixed, moving)

    print("-------")
    print(outTx)
    print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
    print(f" Iteration: {R.GetOptimizerIteration()}")
    print(f" Metric value: {R.GetMetricValue()}")

    # sitk.WriteTransform(outTx, "transform.txt")


    moving_resampled = sitk.Resample(moving, fixed, outTx, sitk.sitkLinear, 0.0, moving.GetPixelID())
    return moving_resampled
    #sitk.WriteImage(moving_resampled, outputFileName)




