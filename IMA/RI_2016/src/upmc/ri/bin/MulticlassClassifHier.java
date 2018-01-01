package upmc.ri.bin;

import java.io.File;
import java.io.IOException;
import java.util.List;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.instantiation.MultiClass;
import upmc.ri.struct.instantiation.MultiClassHier;


public class MulticlassClassifHier extends MulticlassClassif {

	public MulticlassClassifHier(String sourcePath) throws ClassNotFoundException, IOException{
		data = VisualIndexes.loadDataSet(new File(sourcePath));
	}
	
	public MulticlassClassifHier(DataSet<double[], String> dataSet) {
		data = dataSet;
	}
	
	public static MultiClass initMultiClass(List<String> classes){
		return new MultiClassHier(classes);
	}
	
	public static MulticlassClassif initMulticlassClassif(String path) throws ClassNotFoundException, IOException{
		return new MulticlassClassifHier(path);
	}

}
