package upmc.ri.struct.model;

import upmc.ri.struct.instantiation.IStructInstantiation;
import java.util.Random;

public abstract class LinearStructModel<X, Y> implements IStructModel<X, Y> {

	private IStructInstantiation<X, Y> mi;
	private double[] p;
	public Random random = new Random();
	
	public LinearStructModel (int dimpsi) {

		this.p = new double[dimpsi];
        for(int i = 0; i < dimpsi; i++)
            this.p[i] = random.nextDouble();
	}

	public IStructInstantiation<X, Y> instantiation() {
		return this.mi;
	}

	public double[] getParameters() {
		return this.p;
	}

	public void setInstantiation(IStructInstantiation <X,Y> instantiation) {
		this.instantiation = instantiation;
	}
}