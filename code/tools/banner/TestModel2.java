/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package bc2;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import edu.umass.cs.mallet.base.fst.CRF;
import edu.umass.cs.mallet.base.util.MalletLogger;

import banner.BannerProperties;
import banner.Sentence;
import banner.processing.PostProcessor;
import banner.tagging.CRFTagger;
import banner.tagging.Mention;
import banner.tokenization.Tokenizer;

public class TestModel2 extends Base2
{

    /**
     * @param args
     */
    public TestModel2(String[] args) throws IOException
    {
        long startTime = System.currentTimeMillis();
        BannerProperties properties = BannerProperties.load(args[0]);
        BufferedReader sentenceFile = new BufferedReader(new FileReader(args[1]));
        BufferedReader mentionTestFile = new BufferedReader(new FileReader(args[2]));
        BufferedReader mentionAlternateFile = new BufferedReader(new FileReader(args[3]));
        File modelFile = new File(args[4]);
        String directory = args[5];

        properties.log();

        Logger.getLogger(CRF.class.getName()).setLevel(Level.OFF);
        MalletLogger.getLogger(CRF.class.getName()).setLevel(Level.OFF);

        HashMap<String, LinkedList<Base2.Tag>> tags = new HashMap<String, LinkedList<Base2.Tag>>(getTags(mentionTestFile));
        HashMap<String, LinkedList<Base2.Tag>> alternateTags = new HashMap<String, LinkedList<Base2.Tag>>(getAlternateTags(mentionAlternateFile));

        String line = sentenceFile.readLine();
        List<Sentence> sentences = new ArrayList<Sentence>();
        Set<Mention> mentionsTest = new HashSet<Mention>();
        Set<Mention> mentionsAlternate = new HashSet<Mention>();
        while (line != null)
        {
            try {
                int space = line.indexOf(' ');
                String id = line.substring(0, space).trim();
                String sentenceText = line.substring(space).trim();
                Sentence sentence = getSentence(id, sentenceText, properties.getTokenizer(), tags);
                mentionsTest.addAll(sentence.getMentions());
                mentionsAlternate.addAll(getMentions(sentence, alternateTags));
                sentences.add(sentence);
            }
            catch(Exception e) {
                System.out.println("Error occured with line:\n\t" + line);
            }
            line = sentenceFile.readLine();
        }
        sentenceFile.close();

        String outputFilename = directory + "/output.txt";
        String mentionFilename = directory + "/mention.txt";

        PrintWriter outputFile = new PrintWriter(new BufferedWriter(new FileWriter(outputFilename)));
        PrintWriter mentionFile = new PrintWriter(new BufferedWriter(new FileWriter(mentionFilename)));

        Tokenizer tokenizer = properties.getTokenizer();

        CRFTagger tagger = CRFTagger.load(modelFile, properties.getLemmatiser(), properties.getPosTagger());
        PostProcessor postProcessor = properties.getPostProcessor();

        System.out.println("Tagging sentences");
        int count = 0;
        Set<Mention> mentionsFound = new HashSet<Mention>();

        for (Sentence sentence : sentences)
        {
            if (count % 1000 == 0)
                System.out.println(count);
            String sentenceText = sentence.getText();
            try {
                Sentence sentence2 = new Sentence(sentence.getTag(), sentenceText);
                tokenizer.tokenize(sentence2);
                tagger.tag(sentence2);
                if (postProcessor != null)
                    postProcessor.postProcess(sentence2);
                outputFile.println(sentence2.getTrainingText(properties.getTagFormat()));
                mentionsFound.addAll(sentence2.getMentions());
                outputMentions(sentence2, mentionFile);
            }
            catch(Exception e) {
                System.out.println("Error occured with line:\n\t" + sentenceText);
            }
            count++;
        }
        
        outputFile.close();
        mentionFile.close();


        System.out.println("Elapsed time: " + (System.currentTimeMillis() - startTime));

        // double[] results = Base.getResults(mentionsTest, mentionsAlternate,
        // mentionsFound);
        // System.out.println("precision: " + results[1]);
        // System.out.println(" recall: " + results[2]);
        // System.out.println("f-measure: " + results[0]);
    }

}

