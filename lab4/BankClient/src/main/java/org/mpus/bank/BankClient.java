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

        while(true) {
            String input = scanner.nextLine().trim();
            List<String> command = new ArrayList<>(Arrays.asList(input.split("\\s+")));

            if (command.size() == 1) {
                if (input.equalsIgnoreCase("stop")) {
                    break;
                }
                if (input.equalsIgnoreCase("list")) {
                    router.list();
                    continue;
                }
            }
            if (command.size() == 2) {
                switch (command.get(0).toLowerCase()) {
                    case "get" -> router.getBalance(command.get(1));
                    case "add", "delete" -> router.manageAccount(
                        command.get(0).toLowerCase(),
                        command.get(1)
                    );
                    default -> System.out.println("Invalid command");
                }
            }
            else if (command.size() == 3) {
                switch (command.get(0).toLowerCase()) {
                    case "deposit", "withdraw" -> router.manageMoney(
                        command.get(0).toLowerCase(),
                        command.get(1),
                        command.get(2)
                    );
                    default -> System.out.println("Invalid command");
                }
            }
            else {
                System.out.println("Invalid number of arguments");
            }
        }

        router.shutdown();
    }
}
