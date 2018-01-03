import java.io.File;
//import java.util.List;
import java.util.Map;

import upmc.ri.bin.VisualIndexes;
//import upmc.ri.index.ImageFeatures;
//import upmc.ri.index.VIndexFactory;
import upmc.ri.io.ImageNetParser;
import upmc.ri.struct.DataSet;
import upmc.ri.utils.PCA;


public class TME1
{
	public static void main(String[] args) throws Exception
	{
		String dirPath = args[0];
		int nbComp = 250;
		
		Map<String,File> classFileMap = ImageNetParser.getClassFile(dirPath);


		DataSet<double[], String> data = VisualIndexes.createDataSet(classFileMap);
		data = PCA.computePCA(data, nbComp);
		
		VisualIndexes.saveDataSet(new File(dirPath + "dataset.obj"), data);
	}

}
