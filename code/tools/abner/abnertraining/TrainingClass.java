/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package abnertraining;

import abner.Trainer;
/**
 *
 * @author Αλέξανδρος
 */
public class TrainingClass {
    public TrainingClass(String str){
        String file = str + ".iob2";
        String model = str;
        Trainer t = new Trainer();
        t.train(file, model);
    }
}
