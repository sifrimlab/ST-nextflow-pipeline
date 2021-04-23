nextflow.enable.dsl=2

params.stitchDir = "detected_spots_plotted"

include {
    plot_detected_spots; plot_detected_spots_on_tile
 }from "../processes/plotting.nf" 

workflow plot_spots_whole_and_on_tiles {
    take:
        // Data
        detected_spots_seperate
        detected_spots_together
        reference_tiles


        // Tile grid size coordination
        grid_size_x 
        grid_size_y 
        tile_size_x 
        tile_size_y

    main: 
        // Plot on whole image
        plot_detected_spots(detected_spots_together,grid_size_x ,  grid_size_y, tile_size_x, tile_size_y)
        // Plot on seperate tiles
        // For that we map the images and detected spots by their tile number, to be able to match them using join
        reference_tiles.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {reference_tiles_mapped}
        detected_spots_seperate.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {spot_detection_reference_mapped}
        reference_tiles_mapped.join(spot_detection_reference_mapped, by:0).set {tiled_spots_grouped}

        plot_detected_spots_on_tile(tiled_spots_grouped)
}

