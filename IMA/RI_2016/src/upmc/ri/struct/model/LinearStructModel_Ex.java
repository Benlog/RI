package upmc.ri.struct.model;

import upmc.ri.struct.STrainingSample;
import upmc.ri.utils.VectorOperations;
import upmc.ri.struct.instantiation.IStructInstantiation;

public class LinearStructModel_Ex<X, Y> extends LinearStructModel<X, Y>
{
	/**
	 * Initialise un modèle structuré linéaire
	 * 
	 * @param dimpsi Taille des paramètres
	 */
	public LinearStructModel_Ex(int dimpsi)
	{
		super(dimpsi);
	}
	
	/**
	 * Initialise un modèle structuré linéaire
	 * 
	 * @param instantiation	Type de modèle
	 * @param dimpsi Taille des paramètres
	 */
	public LinearStructModel_Ex (IStructInstantiation<X, Y> instantiation, int dimpsi)
	{
		super(instantiation, dimpsi);
	}

	/**
	 * Prédiction de la classe
	 * 
	 * @param ts	Donnée d'entrée
	 * @param lai	Détermine si on applique le loss augmented inference
	 * @return		Prédiction
	 */
	public Y predict(STrainingSample<X, Y> ts, boolean lai)
	{
		Y prediction = null;
		double m = -Double.MAX_VALUE;

		for (Y y : mi.enumerateY())
		{
			double r = VectorOperations.dot(p, mi.psi(ts.input, y));

            if(lai)
                r += mi.delta(y, ts.output);
            
			if (r > m)
			{
				m = r;
				prediction = y;
			}
		}

		return prediction;
	}
	
	/**
	 * Prédiction de la classe sans LAI
	 */
	public Y predict(STrainingSample<X, Y> ts)
	{
		return predict(ts, false);
	}

	/**
	 * Prédiction de la classe avec LAI
	 */
	public Y lai(STrainingSample<X, Y> ts)
	{
		return predict(ts, true);
	}
}