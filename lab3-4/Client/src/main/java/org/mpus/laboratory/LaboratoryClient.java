package org.mpus.laboratory;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class LaboratoryClient {
    public static void main(String[] args) {
        System.out.println("LABORATORY CLIENT");
        System.out.println("Commands:");

        System.out.println("--- Common ---");
        System.out.println("status <type> <id>");
        System.out.println("enable <type> <id>");
        System.out.println("disable <type> <id>");

        System.out.println("--- Camera ---");
        System.out.println("set-pan <id> <value>");
        System.out.println("set-tilt <id> <value>");
        System.out.println("set-zoom <id> <value>");

        System.out.println("--- Irrigation ---");
        System.out.println("set-light <id> <value>");
        System.out.println("set-water <id> <value>");
        System.out.println("set-fertilizer <id> <value>");

        DeviceRouter deviceRouter = new DeviceRouter();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("stop")) {
                break;
            }

            List<String> command = new ArrayList<>(Arrays.asList(input.split("\\s+")));
            if (command.size() != 3) {
                System.out.println("Invalid number of arguments");
                continue;
            }

            switch (command.get(0)) {
                case "status" -> deviceRouter.getStatus(command.get(1), command.get(2));
//                case "enable" -> cameraClient.enableCamera(command.get(1));
//                case "disable" -> cameraClient.disableCamera(command.get(1));
//                case "set-pan" -> cameraClient.setPan(command.get(1), command.get(2));
//                case "set-tilt" -> cameraClient.setTilt(command.get(1), command.get(2));
//                case "set-zoom" -> cameraClient.setZoom(command.get(1), command.get(2));
                default -> System.out.println("Invalid command");
            }
        }

        deviceRouter.shutdownSystem();
    }
}
