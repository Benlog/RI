package upmc.ri.bin;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import upmc.ri.struct.DataSet;
import upmc.ri.struct.Evaluator;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.MultiClass;
import upmc.ri.struct.model.LinearStructModel;
import upmc.ri.struct.model.LinearStructModel_Ex;
import upmc.ri.struct.training.SGDTrainer;
import upmc.ri.bin.VisualIndexes;


public class MulticlassClassif {

	protected DataSet<double[], String> data;
	
	public MulticlassClassif(){
		// (debug classifhier
	}
	
	public MulticlassClassif(String sourcePath) throws ClassNotFoundException, IOException{
		data = VisualIndexes.loadDataSet(new File(sourcePath));
	}
	
	public MulticlassClassif(DataSet<double[], String> dataSet) {
		data = dataSet;
	}
	
	public static MultiClass initMultiClass(List<String> classes){
		return new MultiClass(classes);
	}
	
	public static MulticlassClassif initMulticlassClassif(String path) throws ClassNotFoundException, IOException{
		return new MulticlassClassif(path);
	}

	public static void main(String[] args) throws IOException, ClassNotFoundException {
		//String dirPath = "../../data/sbow/";
		String dirPath = args[0];

		int maxIter = 100;
		double nt = 0.001;
		double lambda = 1;
		
		// Classif
		MulticlassClassif classif = initMulticlassClassif(dirPath + "dataset.obj");
		int dimpsi = classif.data.listtest.get(0).input.length;
		List<String> classes = new ArrayList<String>(classif.data.outputs());
		
		// Multiclass
		MultiClass mc = initMultiClass(classes);
		LinearStructModel<double[], String> lm = new LinearStructModel_Ex<double[], String>(mc, dimpsi * classes.size());

		// OPT
		Evaluator<double[], String> eval = new Evaluator<double[], String>();
		eval.setListtrain(classif.data.listtrain);
		eval.setListtest(classif.data.listtest);
		eval.setModel(lm);
		
		// SGDTrain
		SGDTrainer<double[], String> sgd = new SGDTrainer<double[], String>(maxIter, nt, lambda, eval);
		sgd.train(classif.data.listtrain, lm);
		
		// Eval
		evaluate(lm, eval, classif, mc);
	}
	
	public static void evaluate(LinearStructModel<double[], String> m, Evaluator<double[], String> eval, MulticlassClassif classif, MultiClass mc) {
		eval.evaluate();
		
		System.out.println("Erreur apprentissage : " + String.valueOf(eval.getErr_train()));
		System.out.println("Erreur test          : " + String.valueOf(eval.getErr_test() ));
		
		ArrayList<String> predictions = new ArrayList<String>();
		ArrayList<String> gt = new ArrayList<String>();
		
		for (STrainingSample<double[], String> ts : classif.data.listtest) {
			predictions.add(m.predict(ts));
			gt.add(ts.output);
		}
		
		List<String> classes = new ArrayList<String>(classif.data.outputs());
		m.setInstantiation(initMultiClass(classes));
		eval.setModel(m);
		eval.evaluate();		
		System.out.println("Train Error Hier: " + String.valueOf(eval.getErr_train()));
		System.out.println("Test  Error Hier: " + String.valueOf(eval.getErr_test() ));
		
		mc.confusionMatrix(predictions, gt);
	}

}
