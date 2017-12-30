package upmc.ri.struct.instantiation;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class MultiClass implements IStructInstantiation<double[], String> {
	
	protected Map<String,Integer> classToInt;
	
	public MultiClass(List<String> classes) {
		int cpt = 0;
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
	
}
