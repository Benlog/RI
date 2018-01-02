package upmc.ri.struct.training;

import java.util.List;
import java.util.Random;

import upmc.ri.struct.Evaluator;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.struct.model.IStructModel;
import upmc.ri.utils.VectorOperations;

public class SGDTrainer<X, Y> implements ITrainer<X, Y> {
	
	public Random random = new Random();
	public int maxIter = 100;
	public double nt = 0.001;
	public double lambda = 1;
	public Evaluator<X, Y> evaluator = new Evaluator<X, Y>();
	public boolean verbose = false;
	public List<STrainingSample<X, Y>> test;
	public double[] lossHisto;
	
	public SGDTrainer(int maxIter, double nt, double lambda, Evaluator<X, Y> eval) {
		this.evaluator = eval;
		this.nt = nt;
		this.lambda = lambda;
		this.maxIter = maxIter;
		lossHisto = new double[maxIter];
	}
	
	@Override
	public void train(List<STrainingSample<X, Y>> lts, IStructModel<X, Y> model) {
		int n = lts.size(); 
		
		int gSize = model.getParameters().length;
		
		evaluator.setModel(model);
		evaluator.setListtrain(lts);
		
		System.out.println("Itérations : " + maxIter);
		System.out.println("Ensemble d'apprentissage : " + n);
		
		for(int t = 0; t < maxIter; t++) {
			System.out.println("Itération : " + t);
			double accLoss = 0;
			for (int i = 0; i < n; i++) {
				STrainingSample<X, Y> sample = lts.get(random.nextInt(n));
				Y yPred = model.lai(sample);
				accLoss += model.instantiation().delta(sample.output, yPred);
				
				double[] gPred = model.instantiation().psi(sample.input, yPred);
				double[] gReal = model.instantiation().psi(sample.input, sample.output);
				double[] g = new double[gSize];
				
				for(int j = 0; j < gSize; j++)
					g[j] = gPred[j] - gReal[j];
				
				double[] fg = model.getParameters();

				for(int j = 0; j < gSize; j++)
					fg[j] -= (g[j] + lambda * fg[j]) * nt;
				
				model.setParameters(fg);
			}
			System.out.println("Loss : " + accLoss/n);
			lossHisto[t] = accLoss/n;
			//lossHisto[t] = convex_loss(lts, model);
		}
		System.out.println("Fin apprentissage");
	}
	
	public double convex_loss(List<STrainingSample<X, Y>> lts, IStructModel<X, Y> model) {
		double loss = 0;
		double[] p = model.getParameters();

		IStructInstantiation<X, Y> mi = model.instantiation();
		int n = lts.size(); 

		for (int i = 0; i < n; i++) {
			STrainingSample<X, Y> ts = lts.get(i);

			double m = -Double.MAX_VALUE;

			for (Y y : mi.enumerateY())
				m = Math.max( m, mi.delta(ts.output, y) + VectorOperations.dot(mi.psi(ts.input, y), p) );
			
			loss += m - VectorOperations.dot(mi.psi(ts.input, ts.output), p);
		}

		loss /= lts.size();
		loss += VectorOperations.norm2(p) * this.lambda / 2;

		return loss;
	}

}
