package upmc.ri.bin;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import upmc.ri.index.ImageFeatures;
import upmc.ri.index.VIndexFactory;
import upmc.ri.io.ImageNetParser;
import upmc.ri.struct.DataSet;
import upmc.ri.struct.STrainingSample;

public class VisualIndexes {
	
	public static double trainRatio = 0.8;
	
	@SuppressWarnings("unchecked")
	public static <K> DataSet<double[], K> loadDataSet(File f) throws ClassNotFoundException, IOException{
		try(ObjectInputStream in = new ObjectInputStream(new FileInputStream(f))){
			return (DataSet<double[], K>) in.readObject();
		}
	}
	
	public static <K> void saveDataSet(File f, DataSet<double[], K> data) throws ClassNotFoundException, IOException{
		try(ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(f))){
			out.writeObject(data);
		}
	}
	
	public static <K> DataSet<double[], K> createDataSet(Map<K,File> classFileMap) throws Exception{
		List<STrainingSample<double[], K>> train = new ArrayList<STrainingSample<double[], K>>();
		List<STrainingSample<double[], K>> test = new ArrayList<STrainingSample<double[], K>>();
		for(K k : classFileMap.keySet()){
			List<ImageFeatures> feat =  ImageNetParser.getFeatures(classFileMap.get(k).getAbsolutePath());
			int limit = (int) (feat.size()*trainRatio);
			
			for(int i=0; i < limit; i++){
				double[] histo = VIndexFactory.computeBow(feat.get(i));
				STrainingSample<double[], K> sample = new STrainingSample<double[], K>(histo, k);
				train.add(sample);
			}
			
			for(int i=limit; i < feat.size(); i++){
				double[] histo = VIndexFactory.computeBow(feat.get(i));
				STrainingSample<double[], K> sample = new STrainingSample<double[], K>(histo, k);
				test.add(sample);
			}
		}
		DataSet<double[], K> data = new DataSet<double[], K>(train, test);
		return data;
	}
}
