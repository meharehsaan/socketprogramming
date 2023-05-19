import java.io.*;
import java.util.*;
import java.net.*;

public class sockets {
    public static void main(String[] args) throws IOException {

        ServerSocket ss = new ServerSocket(3737);
        Socket s = ss.accept();
        System.out.println("Server socket created connection");
        DataInputStream dis = null;
        DataOutputStream dos = null;
        try {
            dis = new DataInputStream(s.getInputStream());
            dos = new DataOutputStream(s.getOutputStream());
            // input from user
            String str = " ";
            String str1 = " ";
            Scanner in = new Scanner(System.in);

            while (true) {
                str = dis.readUTF();
                if (str.equals("stop")) {
                    System.out.println("Closing connection... on Clients request");
                    break;
                }
                System.out.println("Client :: " + str);
                System.out.print("Server :: ");
                str1 = in.nextLine();
                dos.writeUTF(str1);
                dos.flush();
            }
        } catch (IOException ex) {
            System.out.println(ex);
        } finally {
            try {
                dis.close();
                dos.close();
                s.close();
                ss.close();
            } catch (IOException e) {
                System.out.println(e);
            }
        }
    }
}
