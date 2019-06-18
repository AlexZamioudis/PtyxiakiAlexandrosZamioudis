/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package abnertraining;

import abner.Tagger;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 *
 * @author Αλέξανδρος
 */
public class TaggingClass {
    public TaggingClass(String str) throws FileNotFoundException, IOException{
        File file = new File(str);
        
        Tagger t = new Tagger(file);
        
        File file1 = new File(str + ".txt"); 
  
        BufferedReader br = new BufferedReader(new FileReader(file1)); 
        BufferedWriter writer = new BufferedWriter(new FileWriter(str + ".sgml"));
        
        String st; 
        while ((st = br.readLine()) != null) 
        {
            writer.write(t.tagSGML(st));
        }
        writer.close();
    }
}
