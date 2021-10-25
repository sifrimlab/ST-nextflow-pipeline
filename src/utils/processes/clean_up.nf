nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process clean_work_dir {

    script:
    """
<<<<<<< HEAD
    python $binDir/clean_work.sh $params.outDir $workDir
=======
    bash $binDir/clean_work.sh $params.outDir $params.workDir
>>>>>>> f7762b51b194849f5aa26c1758620a2de9b882c2
    """
}
