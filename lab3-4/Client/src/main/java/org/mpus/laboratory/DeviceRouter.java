package org.mpus.laboratory;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DeviceRouter {
    private final List<String> servers = new ArrayList<>();
    private final List<ManagedChannel> channels = new ArrayList<>();
    private final List<DeviceRegistryClient> registries = new ArrayList<>();

    private final Map<String, CameraClient> cameraClients = new HashMap<>();
    private final Map<String, IrrigationClient> irrigationClients = new HashMap<>();
    private final Map<String, ACClient> ACClients = new HashMap<>();

    public DeviceRouter() {
        initServers();
        initClients();
    }

    private void initServers() {
        servers.add("localhost:50051");
        servers.add("localhost:50052");
    }

    private void initClients() {
        for (String address : servers) {
            channels.add(ManagedChannelBuilder.forTarget(address)
                    .usePlaintext().build());
        }

        for (ManagedChannel channel : channels) {
            registries.add(new DeviceRegistryClient(channel));
            List<String> ids = registries.get(registries.size() - 1).getDevices();

            CameraClient cameraClient = new CameraClient(channel);
            IrrigationClient irrigationClient = new IrrigationClient(channel);
            ACClient acClient = new ACClient(channel);

            for (String id : ids) {
                cameraClients.put(id, cameraClient);
                irrigationClients.put(id, irrigationClient);
                ACClients.put(id, acClient);
            }
        }
    }

    public void listDevices() {
        for (DeviceRegistryClient registry : registries) {
            for (String device : registry.getDevices()) {
                System.out.println(device);
            }
        }
    }

    public void getStatus(String type, String id) {
        switch (type) {
            case "camera" -> {
                CameraClient cameraClient = cameraClients.get(id);
                if (cameraClient != null) {
                    cameraClient.getCameraStatus(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "irrigation" -> {
                IrrigationClient irrigationClient = irrigationClients.get(id);
                if (irrigationClient != null) {
                    irrigationClient.getIrrigationStatus(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "ac" -> {
                ACClient acClient = ACClients.get(id);
                if (acClient != null) {
                    acClient.getACStatus(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            default -> System.out.println("Unknown type");
        }
    }

    public void enable(String type, String id) {
        switch (type) {
            case "camera" -> {
                CameraClient cameraClient = cameraClients.get(id);
                if (cameraClient != null) {
                    cameraClient.enableCamera(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "irrigation" -> {
                IrrigationClient irrigationClient = irrigationClients.get(id);
                if (irrigationClient != null) {
                    irrigationClient.enableIrrigation(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "ac" -> {
                ACClient acClient = ACClients.get(id);
                if (acClient != null) {
                    acClient.enableAC(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            default -> System.out.println("Unknown type");
        }
    }

    public void disable(String type, String id) {
        switch (type) {
            case "camera" -> {
                CameraClient cameraClient = cameraClients.get(id);
                if (cameraClient != null) {
                    cameraClient.disableCamera(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "irrigation" -> {
                IrrigationClient irrigationClient = irrigationClients.get(id);
                if (irrigationClient != null) {
                    irrigationClient.disableIrrigation(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            case "ac" -> {
                ACClient acClient = ACClients.get(id);
                if (acClient != null) {
                    acClient.disableAC(id);
                }
                else {
                    System.out.println("Device not found");
                }
            }
            default -> System.out.println("Unknown type");
        }
    }

    public void setPan(String id, String value) {
        CameraClient cameraClient = cameraClients.get(id);
        if (cameraClient != null) {
            cameraClient.setPan(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setTilt(String id, String value) {
        CameraClient cameraClient = cameraClients.get(id);
        if (cameraClient != null) {
            cameraClient.setTilt(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setZoom(String id, String value) {
        CameraClient cameraClient = cameraClients.get(id);
        if (cameraClient != null) {
            cameraClient.setZoom(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setLight(String id, String value) {
        IrrigationClient irrigationClient = irrigationClients.get(id);
        if (irrigationClient != null) {
            irrigationClient.setLight(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setWater(String id, String value) {
        IrrigationClient irrigationClient = irrigationClients.get(id);
        if (irrigationClient != null) {
            irrigationClient.setWater(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setFertilizer(String id, String value) {
        IrrigationClient irrigationClient = irrigationClients.get(id);
        if (irrigationClient != null) {
            irrigationClient.setFertilizer(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setTemp(String id, String value) {
        ACClient acClient = ACClients.get(id);
        if (acClient != null) {
            acClient.setTemp(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setFan(String id, String value) {
        ACClient acClient = ACClients.get(id);
        if (acClient != null) {
            acClient.setFan(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void setHumidity(String id, String value) {
        ACClient acClient = ACClients.get(id);
        if (acClient != null) {
            acClient.setHumidity(id, value);
        }
        else {
            System.out.println("Device not found");
        }
    }

    public void shutdownSystem() {
        for (ManagedChannel channel : channels) {
            channel.shutdown();
        }
    }
}
