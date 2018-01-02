package upmc.ri.struct.instantiation;

import java.util.Arrays;
import java.util.List;
import java.util.Set;

import upmc.ri.struct.ranking.RankingFunctions;
import upmc.ri.struct.ranking.RankingOutput;

public class RankingInstantiation implements IStructInstantiation<List<double[]>, RankingOutput> {

	public double[] psi(List<double[]> x, RankingOutput y) {
		double[] r = new double[x.get(0).length];
		Arrays.fill(r, 0);
		int i = 0;
		List<Integer> pos = y.getPositionningFromRanking();
		for (i = 0; i < x.size(); i++) {
			int posi = pos.get(i);
			for (int j = 0; j < x.size(); j++) {
				int posj = pos.get(j);
				int mult = 0;
				if(y.getLabelsGT().get(i) != y.getLabelsGT().get(j)){
					mult = y.getLabelsGT().get(i);
					if (posi < posj)
						mult *= 1;
					else if (posi > posj)
						mult *= -1;
				}
				if (mult != 0)
					for (int j2 = 0; j2 < r.length; j2++) 
						r[j2] +=  mult * x.get(i)[j2];
			}
		}
		return r;
	}

	public double delta(RankingOutput y1, RankingOutput y2) {
		return 1 - RankingFunctions.averagePrecision(y2);
	}

	public Set<RankingOutput> enumerateY() {
		//Not implemented
		throw new UnsupportedOperationException();
	}

}
