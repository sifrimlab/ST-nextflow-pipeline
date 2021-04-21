nextflow.enable.dsl=2

include {
    plot_intensity_histogram; get_intensity_analytics ; collect_intensity_analytics ; create_html_report; plot_combined_histogram ; plot_combined_histogram as plot_combined_channel_histogram
} from "../processes/intensity_processes.nf"

workflow intensity_diagnosing{
  take: 
  glob_pattern

  main: 
  images = Channel.fromPath(glob_pattern)

  plot_intensity_histogram(images)
  all_plots = plot_intensity_histogram.out.collect()
  
  // group images by round 
  images.map { file -> tuple((file =~ /Round\d+/)[0], file)} 
           | groupTuple(by:0)   
           | set {grouped_by_round_images}
  images.map { file -> tuple((file =~ /c\d+/)[0], file)} 
           | groupTuple(by:0)   
           | set {grouped_by_channel_images}
  plot_combined_histogram(grouped_by_round_images)
  plot_combined_channel_histogram(grouped_by_channel_images)
  round_plots = plot_combined_histogram.out.collect()
  channel_plots = plot_combined_channel_histogram.out.collect()

  round_plots.view()
  channel_plots.view()

  get_intensity_analytics(images)
  intensities = get_intensity_analytics.out.collect()

  collect_intensity_analytics(intensities)
  intensity_table = collect_intensity_analytics.out

  create_html_report(params.nr_rounds,params.nr_channels,"$baseDir/assets/html_templates/intensity_report_template.html", intensity_table,round_plots, channel_plots, all_plots)

}   
