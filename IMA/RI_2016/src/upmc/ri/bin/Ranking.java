package upmc.ri.bin;

import java.io.File;
import java.io.IOException;
import java.util.List;

import javax.imageio.ImageIO;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.Evaluator;
import upmc.ri.struct.ranking.RankingFunctions;
import upmc.ri.struct.ranking.RankingOutput;
import upmc.ri.struct.training.SGDTrainer;
import upmc.ri.struct.instantiation.RankingInstantiation;
import upmc.ri.struct.model.RankingStructModel;
import upmc.ri.utils.Drawing;

public class Ranking {
	
	public static void main(String[] args) throws ClassNotFoundException, IOException {
		String objPath  = args[0];
		String selClass = args[1];
		int maxIter = 50;
		double nt = 0.001;
		double lambda = 10;
		
		// chargement données
		DataSet<double[], String> data_index = VisualIndexes.loadDataSet(new File(objPath));
		DataSet<List<double[]>, RankingOutput> data = RankingFunctions.convertClassif2Ranking(data_index, selClass);

		// ranking instantiation
		int dimpsi = data_index.listtest.get(0).input.length;
		RankingInstantiation ri = new RankingInstantiation();
		RankingStructModel rsm = new RankingStructModel(ri, dimpsi);
		
		// OPT
		Evaluator<List<double[]>, RankingOutput> eval = new Evaluator<List<double[]>, RankingOutput>();
		eval.setListtrain(data.listtrain);
		eval.setListtest(data.listtest);
		eval.setModel(rsm);

		// SGDTrain
		SGDTrainer<List<double[]>, RankingOutput> sgd = new SGDTrainer<List<double[]>, RankingOutput>(maxIter, nt, lambda, eval);
		sgd.train(data.listtrain, rsm);
		
		// Eval
		System.out.println("Draw");
		File output = new File("ranking" + selClass + ".png");
		ImageIO.write(Drawing.traceRecallPrecisionCurve(data.listtest.get(0).output.getNbPlus(), RankingFunctions.recalPrecisionCurve(rsm.predict(data.listtest.get(0)))), "PNG", output);
		System.out.println("Précision moyenne :" + RankingFunctions.averagePrecision(rsm.predict(data.listtest.get(0))));
	}

}
