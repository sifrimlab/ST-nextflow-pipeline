nextflow.enable.dsl=2

include {
    plot_intensity_histogram; get_intensity_analytics ; collect_intensity_analytics
} from "../processes/intensity_processes.nf"

workflow intensity_diagnosing{
  take: 
  glob_pattern

  main: 
  images = Channel.fromPath(glob_pattern)

  plot_intensity_histogram(images)

  get_intensity_analytics(images)
  intensities = get_intensity_analytics.out.collect()
  collect_intensity_analytics(intensities)

}   