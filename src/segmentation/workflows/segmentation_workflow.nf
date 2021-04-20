nextflow.enable.dsl=2

include {
    otsu_thresholding ; collect_cell_properties ; assign_genes_to_cells 
} from "../processes/segmentation.nf"

workflow threshold_watershed_segmentation {
    take:
        dapi_images
        decoded_genes
    main:
        // Perform segmentation
        otsu_thresholding(dapi_images)
        collect_cell_properties(otsu_thresholding.out.properties.collect()) //Saves them into a concatenated file

        // Parse the outputs in a way that per tile, one decoded gene file and one labeled image is input into the pipeline
        decoded_genes.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {decoded_genes_mapped}
        otsu_thresholding.out.labeled_images.map {file -> tuple((file.baseName=~ /tiled_\d+/)[0], file)}.set {labeled_images_mapped}
        decoded_genes_mapped.join(labeled_images_mapped, by:0).set{combined}

        assign_genes_to_cells(combined)
        assign_genes_to_cells.out.collectFile(name: "$params.outDir/assigned/concat_assigned_genes.csv", sort:true, keepHeader:true).set {assigned}


    emit: 
        assigned_genes = assign_genes_to_cells.out
        concat_assigned_genes = assigned
        


}
