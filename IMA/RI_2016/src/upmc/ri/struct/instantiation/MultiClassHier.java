package upmc.ri.struct.instantiation;

import java.util.List;

import edu.cmu.lti.lexical_db.ILexicalDatabase;
import edu.cmu.lti.lexical_db.NictWordNet;
import edu.cmu.lti.ws4j.RelatednessCalculator;
import edu.cmu.lti.ws4j.impl.WuPalmer;

public class MultiClassHier extends MultiClass
{
	private double[][] distances;
	
	public double delta(String real, String prediction)
	{
		return distances[classToInt.get(real)][classToInt.get(prediction)];
	}
	
	public MultiClassHier(List<String> classes)
	{
		super(classes);
		
		// initialisation distances
		int n = classToInt.size();
		distances = new double[n][n];
		
		// calcul distances
		ILexicalDatabase ldb = new NictWordNet();
		RelatednessCalculator rc = new WuPalmer(ldb);
		
		// bornes
		double min = Double.MAX_VALUE;
		double max = -Double.MAX_VALUE;
		
		// compute distances
		for (String a : classes)
		{
			int i = classToInt.get(a);
			for (String b : classes)
			{ 
				int j = classToInt.get(b);

				if (i == j) 
					distances[i][j] = 0;
				
				else if (i < j) // économie symétrie et axe à 0
				{
					// dissimilarité
					distances[i][j] = 1 - rc.calcRelatednessOfWords(a, b);
					
					// mesure bornes
					if (distances[i][j] < min)
						min = distances[i][j];

					if (distances[i][j] > max)
						max = distances[i][j];
				}
			}
		}
		
		// normalisation
		double e = max - min;
		double bmin = 0;
		double bmax = 2;
		
		for (int i = 0; i < n; i++)
		{
			for (int j = i+1; j < n; j++)
			{
				distances[i][j] = bmax * (distances[i][j] - min) / e + bmin;
				distances[j][i] = distances[i][j]; // symétrie
			}
		}
		
	}
}
