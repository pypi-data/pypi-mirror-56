import java.util.*;
import ij.io.*;
import ij.gui.*;
import ij.process.*;
public class ReaderROI{

	public static void main(String[] args){
		//System.out.println(args[0]);
		//RoiDecoder rr = new RoiDecoder(args[0]);
		Roi roi = RoiDecoder.open(args[0]);
		FloatPolygon fp = roi.getFloatPolygon();
		for(int i=0; i<fp.npoints; i++){
			System.out.println(fp.xpoints[i] + "," + fp.ypoints[i]);
		}
		
	}


}
