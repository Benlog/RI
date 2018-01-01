package upmc.ri.struct.model;

import upmc.ri.struct.instantiation.IStructInstantiation;

import java.util.Arrays;
import java.util.Random;

public abstract class LinearStructModel<X, Y> implements IStructModel<X, Y> {

	protected IStructInstantiation<X, Y> mi;
	protected double[] p;
	public Random random = new Random();
	
	public LinearStructModel (int dimpsi) {

		p = new double[dimpsi];
		Arrays.fill(p, 0);
        /*for(int i = 0; i < dimpsi; i++)
            this.p[i] = random.nextDouble();
        */
	}

	public IStructInstantiation<X, Y> instantiation() {
		return this.mi;
	}

	public double[] getParameters() {
		return this.p;
	}
	
	public void setParameters(double[] w) {
		this.p = w;
	}

	public void setInstantiation(IStructInstantiation <X,Y> instantiation) {
		this.mi = instantiation;
	}
}