nextflow.enable.dsl=2

include {
    plot_intensity_histogram; get_intensity_analytics ; collect_intensity_analytics ; create_html_report
} from "../processes/intensity_processes.nf"

workflow intensity_diagnosing{
  take: 
  glob_pattern

  main: 
  images = Channel.fromPath(glob_pattern)

  plot_intensity_histogram(images)
  plots = plot_intensity_histogram.out.collect()

  get_intensity_analytics(images)
  intensities = get_intensity_analytics.out.collect()

  collect_intensity_analytics(intensities)
  intensity_table = collect_intensity_analytics.out

  create_html_report("$baseDir/assets/html_report_template.html", intensity_table, plots)

}   