nextflow.enable.dsl=2

params.stitchDir = "detected_spots_plotted"

include {
    plot_detected_spots; plot_detected_spots_on_tile
 }from "../processes/plotting.nf" 

 include { 
    stitch_rgb_tiles
 } from "$baseDir/src/utils/processes/stitching.nf"
 
workflow plot_spots_on_tiles {
    take:
        // Data
        detected_spots
        reference_tiles

        // Tile grid size coordination
        grid_size_x 
        grid_size_y 
        tile_size_x 
        tile_size_y

    main: 
        // Plot on seperate tiles
        reference_tiles.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {reference_tiles_mapped}
        detected_spots.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {spot_detection_reference_mapped}
        reference_tiles_mapped.join(spot_detection_reference_mapped, by:0).set {tiled_spots_grouped}

        plot_detected_spots_on_tile(tiled_spots_grouped)
        //stitch the tiles together for more oversight
        stitch_rgb_tiles(grid_size_x, grid_size_y, tile_size_x, tile_size_y, plot_detected_spots_on_tile.out.collect())
}

/* workflow plot_spots_whole_and_on_tiles { */
/*     take: */
/*         // Data */
/*         detected_spots */
/*         reference_tiles */
/*         blobs */

/*         // Tile grid size coordination */
/*         grid_size_x */ 
/*         grid_size_y */ 
/*         tile_size_x */ 
/*         tile_size_y */

/*     main: */ 
/*         // Plot the whole image */
/*         plot_detected_spots(blobs,grid_size_x, grid_size_y, tile_size_x, tile_size_y) */


/*         // Plot on seperate tiles */
/*         reference_tiles.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {reference_tiles_mapped} */
/*         detected_spots.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {spot_detection_reference_mapped} */
/*         reference_tiles_mapped.join(spot_detection_reference_mapped, by:0).set {tiled_spots_grouped} */

/*         plot_detected_spots_on_tile(tiled_spots_grouped) */
/* } */
