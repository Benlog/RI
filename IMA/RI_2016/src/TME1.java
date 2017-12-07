import java.io.File;
//import java.util.List;
import java.util.Map;

import upmc.ri.bin.VisualIndexes;
//import upmc.ri.index.ImageFeatures;
//import upmc.ri.index.VIndexFactory;
import upmc.ri.io.ImageNetParser;
import upmc.ri.struct.DataSet;
import upmc.ri.utils.PCA;


public class TME1 {
	
	public static void main(String[] args) throws Exception {
		String dirPath = "/users/Etu3/3200403/RI/IMA/RI_2016/data/sbow/";
		int nbComp = 250;
		
		Map<String,File> classFileMap = ImageNetParser.getClassFile(dirPath);
		/*
		List<ImageFeatures> features = ImageNetParser.getFeatures(classFileMap.get(ImageNetParser.classesImageNet().toArray()[0]).getAbsolutePath());
		System.out.println(features);
		double[] histo = VIndexFactory.computeBow(features.get(0));
		System.out.println();
		for (double h : histo){
			System.out.print(h + " ");
		}
		System.out.println();
		*/
		DataSet<double[], String> data = VisualIndexes.createDataSet(classFileMap);
		data = PCA.computePCA(data, nbComp);
		VisualIndexes.saveDataSet(new File("./dataset.obj"), data);
		//System.out.println(VisualIndexes.loadDataSet(new File("./dataset.obj")));
	}

}
