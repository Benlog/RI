import java.util.List;

import upmc.ri.index.ImageFeatures;
import upmc.ri.index.VIndexFactory;
import upmc.ri.io.ImageNetParser;


public class TME1 {

	
	public static void main(String[] args) throws Exception {
		
		List<ImageFeatures> features = ImageNetParser.getFeatures("/users/Etu3/3200403/RI/IMA/RI_2016/data/sbow/acoustic_guitar.txt");
		System.out.println(features);
		double[] histo = VIndexFactory.computeBow(features.get(0));
		System.out.println("");
		for (double h : histo){
			System.out.print(h + " ");
		}
		
	}

}
