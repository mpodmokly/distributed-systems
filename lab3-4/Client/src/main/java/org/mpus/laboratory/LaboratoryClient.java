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
        System.out.println("stop");
        System.out.println("list");
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

        System.out.println("--- AC ---");
        System.out.println("set-temp <id> <value>");
        System.out.println("set-fan <id> <value>");
        System.out.println("set-humidity <id> <value>");

        DeviceRouter deviceRouter = new DeviceRouter();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            String input = scanner.nextLine().trim().toLowerCase();
            if (input.equals("stop")) {
                break;
            }
            if (input.equals("list")) {
                deviceRouter.listDevices();
                continue;
            }

            List<String> command = new ArrayList<>(Arrays.asList(input.split("\\s+")));
            if (command.size() != 3) {
                System.out.println("Invalid number of arguments");
                continue;
            }

            switch (command.get(0)) {
                case "status" -> deviceRouter.getStatus(command.get(1), command.get(2));
                case "enable" -> deviceRouter.enable(command.get(1), command.get(2));
                case "disable" -> deviceRouter.disable(command.get(1), command.get(2));
                case "set-pan" -> deviceRouter.setPan(command.get(1), command.get(2));
                case "set-tilt" -> deviceRouter.setTilt(command.get(1), command.get(2));
                case "set-zoom" -> deviceRouter.setZoom(command.get(1), command.get(2));
                case "set-light" -> deviceRouter.setLight(command.get(1), command.get(2));
                case "set-water" -> deviceRouter.setWater(command.get(1), command.get(2));
                case "set-fertilizer" -> deviceRouter.setFertilizer(command.get(1), command.get(2));
                case "set-temp" -> deviceRouter.setTemp(command.get(1), command.get(2));
                case "set-fan" -> deviceRouter.setFan(command.get(1), command.get(2));
                case "set-humidity" -> deviceRouter.setHumidity(command.get(1), command.get(2));
                default -> System.out.println("Invalid command");
            }
        }

        deviceRouter.shutdownSystem();
    }
}
