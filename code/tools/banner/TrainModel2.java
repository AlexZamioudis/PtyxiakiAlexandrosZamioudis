/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package bc2;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import banner.BannerProperties;
import banner.Sentence;
import banner.tagging.CRFTagger;
import banner.tokenization.Tokenizer;

import edu.umass.cs.mallet.base.fst.CRF;
import edu.umass.cs.mallet.base.util.MalletLogger;

public class TrainModel2 extends Base2
{

    public TrainModel2(String[] args) throws IOException
    {
        BannerProperties properties = BannerProperties.load(args[0]);
        BufferedReader sentenceFile = new BufferedReader(new FileReader(args[1]));
        String tagFilename = args[2];
        String directory = args[3];
        Double percentage = null;
        if (args.length == 5)
            percentage = Double.valueOf(args[4]);

        properties.log();

        Logger.getLogger(CRF.class.getName()).setLevel(Level.OFF);
        MalletLogger.getLogger(CRF.class.getName()).setLevel(Level.OFF);
        
        // Redirect the standard error stream
        PrintStream sysOut = System.out;
        PrintStream fileOut = new PrintStream(new BufferedOutputStream(new FileOutputStream(directory + "/stdout.txt")));
        System.setOut(fileOut);
        PrintStream fileErr = new PrintStream(new BufferedOutputStream(new FileOutputStream(directory + "/stderr.txt")));
        System.setErr(fileErr);
        
        BufferedReader tagFile = new BufferedReader(new FileReader(tagFilename));
        HashMap<String, LinkedList<Base2.Tag>> tags = Base2.getTags(tagFile);
        tagFile.close();
        
        Tokenizer tokenizer = properties.getTokenizer();
        String line = sentenceFile.readLine();
        List<Sentence> sentences = new ArrayList<Sentence>();
        while (line != null)
        {
            if (percentage == null || Math.random() < percentage.doubleValue())
            {
                int space = line.indexOf(' ');
                String id = line.substring(0, space).trim();
                String sentence = line.substring(space).trim();
                try {
                    sentences.add(getSentence(id, sentence, tokenizer, tags));
                }
                catch(Exception e) {
                    sysOut.println("Error occured with line:\n\t" + sentence);
                }
            }
            line = sentenceFile.readLine();
        }
        sentenceFile.close();
        
        sysOut.println("Getting sentence list");

        sysOut.println("Training data loaded, starting training");
        CRFTagger tagger = CRFTagger.train(sentences, properties.getOrder(), properties.isUseFeatureInduction(), properties.getTagFormat(),
                                           properties.getTextDirection(), properties.getLemmatiser(), properties.getPosTagger(),
                                           properties.isUseNumericNormalization());
        sysOut.println("Training complete, saving model");
        tagger.write(new File(directory + "/model.bin"));
    }

}
