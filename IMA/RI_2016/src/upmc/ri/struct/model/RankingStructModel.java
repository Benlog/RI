package upmc.ri.struct.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.struct.ranking.RankingFunctions;
import upmc.ri.struct.ranking.RankingOutput;
import upmc.ri.utils.VectorOperations;

public class RankingStructModel extends LinearStructModel<List<double[]>, RankingOutput>
{
	public RankingStructModel(int dimpsi)
	{
		super(dimpsi);
	}
	
	public RankingStructModel(IStructInstantiation<List<double[]>, RankingOutput> instantiation, int dimpsi)
	{
		super(instantiation, dimpsi);
	}
	
	public RankingOutput predict(STrainingSample<List<double[]>, RankingOutput> ts, boolean lai)
	{
		if(lai)
			return lai(ts);
		return predict(ts);
	}

	@Override
	/**
	 * Prédiction de la classe sans LAI
	 * 
	 * @param ts	Donnée d'entrée
	 * @return
	 */
	public RankingOutput predict(final STrainingSample<List<double[]>, RankingOutput> ts)
	{
		List<Integer> ranking = new ArrayList<Integer>();
		final double[] dot = new double[ts.input.size()];
		
		for (int i = 0; i < ts.input.size(); i++)
		{
			ranking.add(i);
			dot[i] = VectorOperations.dot(p, ts.input.get(i));
		}
		
		Collections.sort(
				ranking, 
				new Comparator<Integer>()
				{
					@Override
					public int compare(Integer i, Integer j)
					{
						if(dot[i] - dot[j] > 0)
							return -1;
						if(dot[i] - dot[j] < 0)
							return 1;
						else 
							return 0;
					}
				});
		
		return new RankingOutput(ts.output.getNbPlus(), ranking, ts.output.getLabelsGT());
	}

	@Override
	/**
	 * Prédiction de la classe avec LAI
	 * 
	 * @param ts	Donnée d'entrée
	 * @return
	 */
	public RankingOutput lai(STrainingSample<List<double[]>, RankingOutput> ts)
	{
		return RankingFunctions.loss_augmented_inference(ts, p);
	}

}
