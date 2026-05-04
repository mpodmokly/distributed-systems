package org.mpus.bank;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class BankClient {
    public static void main(String[] args) {
        System.out.println("BANK CLIENT");
        System.out.println("Commands:");
        System.out.println("stop");
        System.out.println("list");
        System.out.println("[get, add, delete] <owner>");
        System.out.println("[deposit, withdraw] <owner> <amount>");

        Router router = new Router(args);
        Scanner scanner = new Scanner(System.in);

        try {
            while(true) {
                String input = scanner.nextLine().trim().toLowerCase();
                if (input.equals("stop")) {
                    break;
                }
                if (input.equals("list")) {
                    router.list();
                }

                List<String> command = new ArrayList<>(Arrays.asList(input.split("\\s+")));
                if (command.size() == 2) {
                    switch (command.get(0)) {
                        case "get" -> router
                    }
                }
                else if (command.size() == 3) {

                }
                else {
                    System.out.println("Invalid number of arguments");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            router.shutdown();
        }
    }
}
