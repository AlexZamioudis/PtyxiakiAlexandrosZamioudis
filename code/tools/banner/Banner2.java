/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package banner2;

import bc2.TrainModel2;
import bc2.TestModel2;
import java.io.IOException;
/**
 *
 * @author Αλέξανδρος
 */
public class Banner2 {

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    //"banner.properties" "jnlpba.txt" "jnlpba.iob2" "C:\Users\Αλέξανδρος\Documents\NetBeansProjects\banner2"
    public static void main(String[] args) throws IOException {
        ///*
        String[] temp = new String[6];
        temp[0] = "banner.properties";
        temp[1] = "bioinfer_test.txt";
        temp[2] = "bioinfer_test.ann";
        temp[3] = "bioinfer_test1.ann";
        temp[4] = "model.bin";
        temp[5] = "C:\\Users\\Αλέξανδρος\\Documents\\NetBeansProjects\\banner2";
        TestModel2 tm = new TestModel2(temp);
        //*/
        /*
        String[] temp = new String[4];
        temp[0] = "banner.properties";
        temp[1] = "bioinfer_train.txt";
        temp[2] = "bioinfer_train.ann";
        temp[3] = "C:\\Users\\Αλέξανδρος\\Documents\\NetBeansProjects\\banner2";
        TrainModel2 tm = new TrainModel2(temp);
        */
    }
    
}
