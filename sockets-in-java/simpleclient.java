import java.io.*;
import java.net.*;
// import java.util.*;

public class simpleclient {
    public static void main(String[] args) throws IOException, ClassNotFoundException {

        String str = "This is from client";

        Socket cs = new Socket("127.0.0.1", 1037);

        PrintWriter ps = new PrintWriter(cs.getOutputStream(), true);
        ps.println(str);

        BufferedReader bis = new BufferedReader(new InputStreamReader(cs.getInputStream()));
        System.out.println(bis.readLine());
        

        bis.close();
        cs.close();
    }
}
