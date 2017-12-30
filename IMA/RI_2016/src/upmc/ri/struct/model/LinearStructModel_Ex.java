package upmc.ri.struct.model;

import upmc.ri.struct.STrainingSample;
import upmc.ri.utils.VectorOperations;
import upmc.ri.struct.instantiation.IStructInstantiation;

public class LinearStructModel_Ex<X, Y> extends LinearStructModel<X, Y> {

	public LinearStructModel_Ex (IStructInstantiation<X, Y> instantiation, int dimpsi) {
		super(dimpsi);
		this.mi = instantiation;
	}

    public Y predict(STrainingSample<X, Y> ts, boolean lai) {
		Y prediction = null;
		double m = -Double.MAX_VALUE;

		for (Y y : this.mi.enumerateY()) {
			double r = VectorOperations.dot(this.p, this.mi.psi(ts.input, y));

            if(lai)
                r += this.mi.delta(y, ts.output);
            
			if (r > m) {
				m = r;
				prediction = y;
			}
		}

		return prediction;
	}
	
	public Y predict(STrainingSample<X, Y> ts) {
		return predict(ts, false);
	}

	public Y lai(STrainingSample<X, Y> ts) {
		return predict(ts, true);
	}
}