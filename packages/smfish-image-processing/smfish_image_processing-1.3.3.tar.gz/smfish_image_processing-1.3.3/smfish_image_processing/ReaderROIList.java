import java.util.*;
import java.io.*;
import ij.io.*;
import ij.gui.*;
import ij.process.*;
public class ReaderROIList{

	public static void main(String[] args) throws IOException{
		//System.out.println(args[0]);
		//RoiDecoder rr = new RoiDecoder(args[0]);

		Vector<String> files = new Vector<String>();
		BufferedReader in = null;
		try{
			in = new BufferedReader(new FileReader(args[0]));
			String s = null;
			while((s=in.readLine())!=null){
				files.add(s);
			}
		}catch(IOException e){
			System.out.println("Bad IO");
			return ;
		}finally{
			if(in!=null) in.close();
		}

		for(int i=0; i<files.size(); i++){
			Roi roi = RoiDecoder.open(files.get(i));
			FloatPolygon fp = roi.getFloatPolygon();
			for(int j=0; j<fp.npoints; j++){
				System.out.println((i+1) + "," + fp.xpoints[j] + "," + fp.ypoints[j]);
			}
		}
		
	}


}
