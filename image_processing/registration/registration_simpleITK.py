import SimpleITK as sitk
import sys
import os


def calculateRigidTransform(ref: str, target: str, round: int, channel: int, output_dir: str = "", silent=False):
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

    if not silent:
        # print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
        print(f"Calculating transform of round {round}, channel {channel}...")
        print(f"Finished at iteration {R.GetOptimizerIteration()} with a metric value of {R.GetMetricValue()}")

    sitk.WriteTransform(outTx, f"{output_dir}transform_r{round}_c{channel}.txt")

    print(f"Transform written to {output_dir}transform_r{round}_c{channel}.txt \n")

    ## important commands for future transform use:
    #read_result = sitk.ReadTransform('euler2D.tfm')
    #moving_resampled = sitk.Resample(moving, fixed, result, sitk.sitkLinear, 0.0, moving.GetPixelID())
    #sitk.WriteImage(moving_resampled, outputFileName)


def writeRigidTransformed(target_img_path: str, transform_file: str, output_file: str):
    """Warps the given image with the given transformation and writes the warped image to the destination file.

    Parameters
    ----------
    target_img_path : str
        Path leading to the image to be warped.
    transform_file : str
        Path leading to the tranformation file.
    output_file : str
        Path where the warped image will be written
    """
    # Read in image to be warped
    target = sitk.ReadImage(target_img_path, sitk.sitkFloat32)
    # Read in transformation to do it with
    read_result = sitk.ReadTransform(transform_file)
    # Resample (warp) the image
    resampled = sitk.Resample(target, read_result, sitk.sitkLinear, 0.0, target.GetPixelID())
    # Write image to the given destination
    sitk.WriteImage(resampled, output_file)
    print(f"Warped image written to {output_file}.")