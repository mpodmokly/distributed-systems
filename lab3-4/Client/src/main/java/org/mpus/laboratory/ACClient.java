package org.mpus.laboratory;

import io.grpc.ManagedChannel;
import io.grpc.StatusRuntimeException;

public class ACClient {
    private final ACServiceGrpc.ACServiceBlockingStub stub;

    public ACClient(ManagedChannel channel) {
        stub = ACServiceGrpc.newBlockingStub(channel);
    }

    public void getACStatus(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            ACStatus response = stub.getACStatus(request);
            System.out.println("AC status:");
            System.out.println("ID: " + response.getId().getId());
            System.out.println("Power: " + response.getIsOn());
            System.out.println("Current temp: " + response.getCurrentTemp());
            System.out.println("Target temp: " + response.getTargetTemp());

            switch (response.getTypeDetalisCase()) {
                case BASIC -> {}
                case ADVANCED -> {
                    FanMode fan = response.getAdvanced().getFanMode();
                    int current_humidity = response.getAdvanced().getCurrentHumidity();
                    int target_humidity = response.getAdvanced().getTargetHumidity();
                    System.out.println("Fan mode: " + fan);
                    System.out.println("Current humidity: " + current_humidity);
                    System.out.println("Target humidity: " + target_humidity);
                }
                case TYPEDETALIS_NOT_SET -> System.out.println("No AC type set");
            }
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void enableAC(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.enableAC(request);
            System.out.println("AC " + id + " enabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void disableAC(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.disableAC(request);
            System.out.println("AC " + id + " disabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setTemp(String id, String temp) {
        int tempVal;
        try {
            tempVal = Integer.parseInt(temp);
        } catch (NumberFormatException e) {
            System.out.println("Invalid temp value");
            return;
        }

        if (tempVal < 5 || tempVal > 25) {
            System.out.println("Temp value must be between 5-25");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetACTempRequest request = SetACTempRequest.newBuilder()
                .setId(deviceID).setTargetTemp(tempVal).build();
        try {
            stub.setACTemp(request);
            System.out.println("Set AC " + id + " temp to " + tempVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setFan(String id, String fan) {
        FanMode fanMode;
        try {
            fanMode = FanMode.valueOf(fan.toUpperCase());
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid fan mode");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetACFanRequest request = SetACFanRequest.newBuilder()
                .setId(deviceID).setFanMode(fanMode).build();
        try {
            stub.setACFan(request);
            System.out.println("Set AC " + id + " fan to " + fanMode);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setHumidity(String id, String humidity) {
        int humidityVal;
        try {
            humidityVal = Integer.parseInt(humidity);
        } catch (NumberFormatException e) {
            System.out.println("Invalid humidity value");
            return;
        }

        if (humidityVal < 0 || humidityVal > 100) {
            System.out.println("Humidity value must be between 0-100");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetACHumidityRequest request = SetACHumidityRequest.newBuilder()
                .setId(deviceID).setTargetHumidity(humidityVal).build();
        try {
            stub.setACHumidity(request);
            System.out.println("Set AC " + id + " humidity to " + humidityVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }
}
