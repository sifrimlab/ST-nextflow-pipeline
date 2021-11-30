nextflow.enable.dsl=2

include {
    otsu_thresholding ; collect_cell_properties ; assign_genes_to_cells; assign_genes_to_cells_voronoi; stardist_segmentation; create_count_matrix 
} from "../processes/segmentation.nf"

include{
    plot_segmentation_labels ; plot_segmentation_labels_on_ref; plot_segmentation_labels_on_dapi ; plot_assigned_genes
} from "$baseDir/src/plotting/processes/plotting.nf"

include {
    transform_tile_coordinate_system
} from "$baseDir/src/file_conversion/processes/coordinate_parsing.nf"

include {
    umap ; find_seurat_clusters
} from "$baseDir/src/downstream_analysis/processes/downstream_analysis.nf"

workflow merfish_threshold_watershed_segmentation {
    take:
        dapi_images
        decoded_genes

        // Tile grid parameters for stitching
        grid_size_x
        grid_size_y
        tile_size_x
        tile_size_y

    main:
        // Perform segmentation
        otsu_thresholding(dapi_images)
        collect_cell_properties(otsu_thresholding.out.properties.collect()) //Saves them into a concatenated file

        decoded_genes.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {decoded_genes_mapped}
        otsu_thresholding.out.labeled_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {labeled_images_mapped}
        otsu_thresholding.out.properties.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {cell_properties_mapped}
        dapi_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {dapi_images_mapped}


        labeled_images_mapped.join(dapi_images_mapped, by:0).set{combined_dapi_labeled_images}
        decoded_genes_mapped.join(labeled_images_mapped, by:0).set{combined_decoded_genes}
        combined_decoded_genes.join(cell_properties_mapped, by:0).set{combined_decoded_labeled_properties}



        if (params.plot==true){
            plot_segmentation_labels_on_dapi(combined_dapi_labeled_images) 
            plot_segmentation_labels(otsu_thresholding.out.labeled_images)
        }

        assign_genes_to_cells(combined_decoded_labeled_properties)
        assign_genes_to_cells.out.collectFile(name: "$params.outDir/assigned/concat_assigned_genes.csv", sort:true, keepHeader:true).set {assigned}
        transform_tile_coordinate_system(assigned, grid_size_x, grid_size_y, tile_size_x, tile_size_y).set {assigned_genes}

        create_count_matrix(assigned_genes)
        /* umap(create_count_matrix.out) */
        /* find_seurat_clusters(create_count_matrix.out) */
        emit:
            concat_assigned_genes = assigned
            count_matrix = create_count_matrix.out
                
}

workflow threshold_watershed_segmentation {
    take:
        dapi_images
        decoded_genes
        ref_images

        // Tile grid parameters for stitching
        grid_size_x
        grid_size_y
        tile_size_x
        tile_size_y
    main:
        // Perform segmentation
        otsu_thresholding(dapi_images)
        collect_cell_properties(otsu_thresholding.out.properties.collect()) //Saves them into a concatenated file

        // Parse the outputs in a way that per tile, one decoded gene file and one labeled image is input into the pipeline
        decoded_genes.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {decoded_genes_mapped}
        otsu_thresholding.out.labeled_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {labeled_images_mapped}
        otsu_thresholding.out.properties.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {cell_properties_mapped}
        dapi_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {dapi_images_mapped}
        ref_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {ref_images_mapped}

        labeled_images_mapped.join(dapi_images_mapped, by:0).set{combined_dapi_labeled_images}
        labeled_images_mapped.join(ref_images_mapped, by:0).set{combined_ref_labeled_images}
        decoded_genes_mapped.join(labeled_images_mapped, by:0).set{combined_decoded_genes}
        combined_decoded_genes.join(cell_properties_mapped, by:0).set{combined_decoded_labeled_properties}

        if (params.plot==true){
            plot_segmentation_labels_on_dapi(combined_dapi_labeled_images) 
            /* plot_segmentation_on_ref(combined_ref_labeled_images) */ 
        }

        assign_genes_to_cells_voronoi(combined_decoded_labeled_properties)
        assign_genes_to_cells_voronoi.out.collectFile(name: "$params.outDir/assigned/concat_assigned_genes.csv", sort:true, keepHeader:true).set {assigned}
        transform_tile_coordinate_system(assigned, grid_size_x, grid_size_y, tile_size_x, tile_size_y).set {assigned_genes}

        create_count_matrix(assigned_genes)
        /* umap(create_count_matrix.out) */
        /* find_seurat_clusters(create_count_matrix.out) */

        
        /* assign_genes_to_cells.out.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {assigned_genes_mapped} */
        /* assigned_genes_mapped.join(labeled_images_mapped, by:0).set {combined_assigned_genes} */

        /* plot_assigned_genes(combined_assigned_genes) */

    emit: 
        assigned_genes = assign_genes_to_cells_voronoi.out
        concat_assigned_genes = assigned
        count_matrix = create_count_matrix.out
}

workflow stardist_segmentation_workflow {
    take:
        dapi_images
        decoded_genes
        ref_images

        // Tile grid parameters for stitching
        grid_size_x
        grid_size_y
        tile_size_x
        tile_size_y
    main:
        // Perform segmentation
        stardist_segmentation(dapi_images)
        collect_cell_properties(stardist_segmentation.out.properties.collect()) //Saves them into a concatenated file

        // Parse the outputs in a way that per tile, one decoded gene file and one labeled image is input into the pipeline
        decoded_genes.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {decoded_genes_mapped}
        stardist_segmentation.out.labeled_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {labeled_images_mapped}
        stardist_segmentation.out.properties.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {cell_properties_mapped}
        dapi_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {dapi_images_mapped}
        /* ref_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {ref_images_mapped} */

        // Cobmine all segmentation results and decoded genes by tile, such that everything after this can happen correctly per Tile
        labeled_images_mapped.join(dapi_images_mapped, by:0).set{combined_dapi_labeled_images}
        /* labeled_images_mapped.join(ref_images_mapped, by:0).set{combined_ref_labeled_images} */
        decoded_genes_mapped.join(labeled_images_mapped, by:0).set{combined_decoded_genes}
        combined_decoded_genes.join(cell_properties_mapped, by:0).set{combined_decoded_labeled_properties}

        if (params.plot == true){
            plot_segmentation_labels_on_dapi(combined_dapi_labeled_images) 
            /* plot_segmentation_labels_on_ref(combined_ref_labeled_images) */ 
        }

        assign_genes_to_cells_voronoi(combined_decoded_labeled_properties)
        assign_genes_to_cells_voronoi.out.collectFile(name: "$params.outDir/assigned/concat_assigned_genes.csv", sort:true, keepHeader:true).set {assigned}
        transform_tile_coordinate_system(assigned, grid_size_x, grid_size_y, tile_size_x, tile_size_y).set {assigned_genes}

        create_count_matrix(assigned_genes)
        /* umap(create_count_matrix.out) */
        /* find_seurat_clusters(create_count_matrix.out) */


        // Plot assigned genes doesnt work yet, something with running out of memory problem 
        /* assign_genes_to_cells.out.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {assigned_genes_mapped} */
        /* assigned_genes_mapped.join(labeled_images_mapped, by:0).set {combined_assigned_genes} */

        /* plot_assigned_genes(combined_assigned_genes) */

    emit: 
        assigned_genes = assign_genes_to_cells_voronoi.out
        concat_assigned_genes = assigned
        count_matrix = create_count_matrix.out
}
