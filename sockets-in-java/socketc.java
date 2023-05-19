import java.util.*;
import java.io.*;
import java.net.*;

public class socketc {
    public static void main(String[] args) throws IOException {
        String str = " ";
        String str1 = " ";
        Socket cs = new Socket("127.0.0.1", 3737);

        DataInputStream dis = null;
        DataOutputStream dos = null;

        try {
            Scanner in = new Scanner(System.in);
            dis = new DataInputStream(cs.getInputStream());
            dos = new DataOutputStream(cs.getOutputStream());

            // BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

            while (true) {
                System.out.print("Client :: ");
                str = in.nextLine();
                //writind data to input stream
                if (str.equals("stop")) {
                    dos.writeUTF(str);
                    dos.flush();
                    System.out.println("Closing Connection...");
                    break;
                }
                dos.writeUTF(str);
                dos.flush();
                //reading data from inputstream
                str1 = dis.readUTF();
                System.out.println("Server :: " + str1);
            }
        } catch (IOException ex) {
            System.out.println(ex);
        } finally {
            try {
                dis.close();
                dos.close();
                cs.close();
                // br.close();
            } catch (IOException e) {
                System.out.println(e);
            }
        }
    }
}
