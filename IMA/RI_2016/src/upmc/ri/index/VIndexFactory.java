package upmc.ri.index;

public class VIndexFactory {
	
	public static double[] computeBow(ImageFeatures ib){
		double[] r = new double[ImageFeatures.tdico];
		for (int i = 0; i < r.length; i++) {
			r[i] = 0d;
		}
		for (int l : ib.getwords()){
			r[l] ++;
		}
		for (int i = 0; i < r.length; i++) {
			r[i] /= ib.getwords().size();
		}
		return r;
	}
}
