import SimpleITK as sitk
import sys
import os


def rigid_registration(ref: str, target: str, round: int, channel: int, output_dir: str = ""):
    """Calculates and writes the rigid transformation necessary to register the target onto the reference. 

    Parameters
    ----------
    ref : str
        Path to reference image.
    target : str
        Path to target image to be moved.
    round : int
        Respective round of the target image. (To be used in naming the transformations)
    channel : int
        Respective channel of the target image. (To be used in naming the transformations)
    output_dir : str, optional
        Directory where the transformation will be written to. By default this is "", which is functionaly the current working directory.
    """
    fixed = sitk.ReadImage(ref, sitk.sitkFloat32)

    moving = sitk.ReadImage(target, sitk.sitkFloat32)

    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
    R.SetInterpolator(sitk.sitkLinear)

    outTx = R.Execute(fixed, moving)

    # print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
    print(f"Calculating transform of round {round}, channel {channel}...")
    print(f"Finished at iteration {R.GetOptimizerIteration()} with a metric value of {R.GetMetricValue()}")

    sitk.WriteTransform(outTx, f"{output_dir}transform_r{round}_c{channel}.txt")

    print(f"Transform written to {output_dir}transform_r{round}_c{channel}.txt")

    ## important commands for future transform use:
    #sitk.WriteImage(moving_resampled, outputFileName)
    #read_result = sitk.ReadTransform('euler2D.tfm')
    #moving_resampled = sitk.Resample(moving, fixed, result, sitk.sitkLinear, 0.0, moving.GetPixelID())