nextflow.enable.dsl=2

include {
    plot_intensity_histogram
} from "../processes/intensity_processes.nf"

workflow intensity_diagnosing{
  take: 
  glob_pattern

  main: 
  images = Channel.fromPath(glob_pattern)

  plot_intensity_histogram(images)
}   