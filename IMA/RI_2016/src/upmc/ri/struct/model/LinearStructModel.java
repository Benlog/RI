package upmc.ri.struct.model;

import upmc.ri.struct.instantiation.IStructInstantiation;

import java.util.Arrays;
import java.util.Random;

public abstract class LinearStructModel<X, Y> implements IStructModel<X, Y>
{
	protected IStructInstantiation<X, Y> mi;
	protected double[] p;
	
	/**
	 * Initialise un modèle structuré linéaire
	 * 
	 * @param dimpsi Taille des paramètres
	 */
	public LinearStructModel (int dimpsi)
	{
		initParameters(dimpsi);
	}
	
	/**
	 * Initialise un modèle structuré linéaire
	 * 
	 * @param instantiation	Type de modèle
	 * @param dimpsi Taille des paramètres
	 */
	public LinearStructModel (IStructInstantiation<X, Y> instantiation, int dimpsi)
	{
		initParameters(dimpsi);
		mi = instantiation;
	}

	public IStructInstantiation<X, Y> instantiation()
	{
		return mi;
	}

	public double[] getParameters()
	{
		return p;
	}
	
	public void setParameters(double[] w)
	{
		p = w;
	}
	
	/**
	 * Initialise les paramètres à zéro
	 * 
	 * @param dimpsi Taille des paramètres
	 */
	public void initParameters(int dimpsi)
	{
		initParameters(dimpsi, false);
	}
	
	/**
	 * Initialise les paramètres
	 * 
	 * @param dimpsi Taille des paramètres
	 * @param random Paramètres aléatoires (à zéro sinon)
	 */
	public void initParameters(int dimpsi, boolean random)
	{
		p = new double[dimpsi];
		if(random)
		{
			Random rand = new Random();
			for(int i = 0; i < dimpsi; i++)
				p[i] = rand.nextDouble();
		}
		else
			Arrays.fill(p, 0);
	}

	public void setInstantiation(IStructInstantiation <X,Y> instantiation)
	{
		mi = instantiation;
	}
}