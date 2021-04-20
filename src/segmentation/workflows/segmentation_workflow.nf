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

        decoded_genes.view()
        otsu_thresholding.out.labeled_images.view()
        /* assign_genes_to_cells(decoded_genes, otsu_thresholding.out.labeled_images) */

    /* emit: */ 
    /*     assigned_genes = assign_genes_to_cells.out */
        


}
