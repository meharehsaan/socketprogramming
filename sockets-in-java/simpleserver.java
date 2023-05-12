import java.io.*;
import java.net.*;
import java.util.*;

public class simpleserver {
    public static void main(String[] args) throws IOException, ClassNotFoundException {

        String str = "This is a message from server towards client";

        ServerSocket ss = new ServerSocket(1037);
        System.out.println("Server is listening...");
        Socket c = ss.accept();
        System.out.println("Connection Established...");
        
        BufferedReader bis = new BufferedReader(new InputStreamReader(c.getInputStream()));
        System.out.println(bis.readLine());

        PrintWriter ps = new PrintWriter(c.getOutputStream(), true);
        ps.println(str);
        

        c.close();
        bis.close();
        // ss.close();
    }
}
