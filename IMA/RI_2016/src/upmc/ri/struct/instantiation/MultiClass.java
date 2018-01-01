package upmc.ri.struct.instantiation;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.ejml.data.D1Matrix64F;
import org.ejml.data.DenseMatrix64F;

public class MultiClass implements IStructInstantiation<double[], String> {
	
	public final Map<String,Integer> classToInt;
	
	public MultiClass(List<String> classes) {
		int cpt = 0;
		this.classToInt = new HashMap<String, Integer>();
		for(String c : classes) {
			classToInt.put(c, cpt);
			cpt++;
		}
	}

	public double[] psi(double[] x, String y) {
		int d = x.length;
		int classInt = classToInt.get(y);
		double[] r = new double[classToInt.size() * d];
		Arrays.fill(r, 0);
		for(int i = 0; i < x.length; i++)
			r[classInt * d + i] = x[i];
		return r;
	}

	public double delta(String y1, String y2) {
		return y1.equals(y2) ? 1 : 0;
	}

	public Set<String> enumerateY() {
		return classToInt.keySet();
	}
	

	
	public D1Matrix64F confusionMatrix(List<String> predictions, List<String> gt) {
		int s = classToInt.size();
		D1Matrix64F c = new DenseMatrix64F(s, s);
		
		// init 0
		for (String i : predictions) {
			for (String j : gt)
				c.set(classToInt.get(i), classToInt.get(j), 0);
		}
		
		// confusion
		for (int i = 0; i < gt.size(); i++) {
			int prediction = classToInt.get(predictions.get(i));
			System.out.println();
			int gti = classToInt.get(gt.get(i));
			c.set(prediction, gti, c.get(prediction, gti) + 1);
		}
		
		return c;
	}
	
}
