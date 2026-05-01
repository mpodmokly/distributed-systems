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

    private final Map<String, DeviceRegistryClient> devicesRegistry = new HashMap<>();
    private final Map<String, CameraClient> cameraClients = new HashMap<>();
//    private final Map<String, >

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
            DeviceRegistryClient deviceRegistryClient = new DeviceRegistryClient(channel);
            List<String> ids = deviceRegistryClient.getDevices();

            for (String id : ids) {
                devicesRegistry.put(id, deviceRegistryClient);
                cameraClients.put(id, new CameraClient(channel));
            }
        }
    }

    public void getStatus(String type, String id) {
        switch (type) {
            case "camera" -> cameraClients.get(id).getCameraStatus(id);
        }
    }

    public void shutdownSystem() {
        for (ManagedChannel channel : channels) {
            channel.shutdown();
        }
    }
}
