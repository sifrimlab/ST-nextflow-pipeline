import SimpleITK as sitk
import sys
import os

def register_simpleITK(ref: str, target: str, round: int, channel: int):
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

    sitk.WriteTransform(outTx, "transform.txt")
    # for future use: reading is with read_result = sitk.ReadTransform('euler2D.tfm')
    moving_resampled = sitk.Resample(moving, fixed, result, sitk.sitkLinear, 0.0, moving.GetPixelID())
    return moving_resampled
    #sitk.WriteImage(moving_resampled, outputFileName)

test = register_simpleITK(ref, target)


