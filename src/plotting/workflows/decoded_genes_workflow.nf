nextflow.enable.dsl=2

include {
    plot_decoded_spots as plot_decoded_spots_on_whole_image ;plot_decoded_genes_on_tile 
} from "../processes/plotting.nf" 
 
workflow plot_decoded_genes {
        take: 
            // Data
            reference_tiles
            decoded_genes
            whole_ref_image
            // tile grid 
            grid_size_x
            grid_size_y
            tile_size_x
            tile_size_y
        main:
            
            // To plot decoding, we will have to group decoding data and ref tiles together
            reference_tiles.map{file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {reference_tiles_mapped}
            decoded_genes.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {decoded_genes_mapped}
            reference_tiles_mapped.join(decoded_genes_mapped, by:0).set {tiled_decoded_grouped}

            plot_decoded_genes_on_tile(tiled_decoded_grouped)
            plot_decoded_spots_on_whole_image(decoded_genes, whole_ref_image, grid_size_x, grid_size_y, tile_size_x, tile_size_y)
}
