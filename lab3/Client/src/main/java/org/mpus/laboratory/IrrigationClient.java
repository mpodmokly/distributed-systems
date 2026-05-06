package org.mpus.laboratory;

import io.grpc.ManagedChannel;
import io.grpc.StatusRuntimeException;

public class IrrigationClient {
    private final IrrigationServiceGrpc.IrrigationServiceBlockingStub stub;

    public IrrigationClient(ManagedChannel channel) {
        stub = IrrigationServiceGrpc.newBlockingStub(channel);
    }

    public void getIrrigationStatus(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            IrrigationStatus response = stub.getIrrigationStatus(request);
            System.out.println("Irrigation status:");
            System.out.println("ID: " + response.getId().getId());
            System.out.println("Power: " + response.getIsOn());
            System.out.println("Light: " + response.getLight());

            switch (response.getTypeDetalisCase()) {
                case WATER_TYPE -> {
                    int flow = response.getWaterType().getWaterFlow();
                    System.out.println("Water flow: " + flow);
                }
                case FERTILIZER_TYPE -> {
                    int fertilizer = response.getFertilizerType().getFertilizerRatio();
                    System.out.println("Fertilizer ratio: " + fertilizer);
                }
                case TYPEDETALIS_NOT_SET -> System.out.println("No irrigation type set");
            }
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void enableIrrigation(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.enableIrrigation(request);
            System.out.println("Irrigation " + id + " enabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void disableIrrigation(String id) {
        DeviceID request = DeviceID.newBuilder().setId(id).build();
        try {
            stub.disableIrrigation(request);
            System.out.println("Irrigation " + id + " disabled");
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setLight(String id, String light) {
        LightMode lightMode;
        try {
            lightMode = LightMode.valueOf(light.toUpperCase());
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid light mode");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetLightModeRequest request = SetLightModeRequest.newBuilder()
                .setId(deviceID).setLight(lightMode).build();
        try {
            stub.setLightMode(request);
            System.out.println("Set irrigation " + id + " light to " + lightMode);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setWater(String id, String water) {
        int waterVal;
        try {
            waterVal = Integer.parseInt(water);
        } catch (NumberFormatException e) {
            System.out.println("Invalid water value");
            return;
        }

        if (waterVal < 0 || waterVal > 1000) {
            System.out.println("Water value must be between 0-1000");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetWaterFlowRequest request = SetWaterFlowRequest.newBuilder()
                .setId(deviceID).setWaterFlow(waterVal).build();
        try {
            stub.setWaterFlow(request);
            System.out.println("Set irrigation " + id + " water to " + waterVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }

    public void setFertilizer(String id, String fertilizer) {
        int fertilizerVal;
        try {
            fertilizerVal = Integer.parseInt(fertilizer);
        } catch (NumberFormatException e) {
            System.out.println("Invalid fertilizer value");
            return;
        }

        if  (fertilizerVal < 0 || fertilizerVal > 100) {
            System.out.println("Fertilizer value must be between 0-100");
            return;
        }

        DeviceID deviceID = DeviceID.newBuilder().setId(id).build();
        SetFertilizerRatioRequest request = SetFertilizerRatioRequest.newBuilder()
                .setId(deviceID).setFertilizerRatio(fertilizerVal).build();
        try {
            stub.setFertilizerRatio(request);
            System.out.println("Set irrigation " + id + " fertilizer to " + fertilizerVal);
        } catch (StatusRuntimeException e) {
            System.out.println(e.getStatus().getDescription());
        }
    }
}
